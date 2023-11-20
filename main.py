import math
import time
import random

import pygame
from config import settings as s

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
WIN_BG = pygame.transform.scale(pygame.image.load("assets/background/bg_black.png"), (s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Wave Defence v1")


class Player:
    def __init__(self, x, y, vel=s.PLAYER_VEL):
        self.rect = pygame.Rect(x, y, s.PLAYER_WIDTH, s.PLAYER_HEIGHT)
        self.vel = vel
        self.move = True
        self.current_health = 100


class Weapon:
    def __init__(self, x, y, vel=s.PLAYER_VEL):
        self.rect = pygame.Rect(x, y, s.WEAPON_WIDTH, s.WEAPON_HEIGHT)
        self.vel = vel


class Bullet:
    def __init__(self, x, y, angle, vel):
        self.original_image = pygame.Surface((s.BULLET_WIDTH, s.BULLET_HEIGHT), pygame.SRCALPHA)
        pygame.draw.rect(self.original_image, "blue", (0, 0, s.BULLET_WIDTH, s.BULLET_HEIGHT))
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center=(x, y))
        self.vel = vel
        self.total_damage = 20

    def move(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]


class Obstacle:
    def __init__(self, x, y, model_id):
        self.rect = pygame.Rect(x, y, s.BOX_WIDTH, s.BOX_HEIGHT)
        self.model_id = model_id
        self.hit_points = 100


class Enemy:
    def __init__(self, x, y, model_id, vel=s.ENEMY_VEL):
        self.rect = pygame.Rect(x, y, s.BOX_WIDTH, s.BOX_HEIGHT)
        self.model_id = model_id
        self.hit_points = 50
        self.vel = vel
        self.max_damage = 10

    def move_towards_player(self, player_rect):
        angle = math.atan2(player_rect.centery - self.rect.centery, player_rect.centerx - self.rect.centerx)
        vel_x = self.vel * math.cos(angle)
        vel_y = self.vel * math.sin(angle)
        self.rect.x += vel_x
        self.rect.y += vel_y


def calculate_bullet_velocity(player_pos, mouse_pos, bullet_speed):
    angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
    vel_x = bullet_speed * math.cos(angle)
    vel_y = bullet_speed * math.sin(angle)
    return vel_x, vel_y


def check_bullet_obstacle_collision(bullets, obstacles):
    for bullet in bullets:
        for obstacle in obstacles:
            if bullet.rect.colliderect(obstacle.rect):
                obstacle.hit_points -= bullet.total_damage
                if obstacle.hit_points <= 0:
                    obstacles.remove(obstacle)
                bullets.remove(bullet)
                return True
    return False


def check_player_obstacle_collision(player, obstacles):
    for obstacle in obstacles:
        if player.rect.colliderect(obstacle.rect):
            if player.vel > 0:
                player.rect.bottom = obstacle.rect.top
            elif player.vel < 0:
                player.rect.top = obstacle.rect.bottom
            if player.rect.right > obstacle.rect.left > player.rect.left:
                player.rect.right = obstacle.rect.left
            elif player.rect.left < obstacle.rect.right < player.rect.right:
                player.rect.left = obstacle.rect.right


def check_player_enemy_collision(player, enemy_list):
    for enemy in enemy_list:
        if enemy.rect.colliderect(player.rect):
            player.current_health -= enemy.max_damage


def draw(player, weapon, bullet_list, obstacle_list, enemy_list):
    WIN.blit(WIN_BG, (0, 0))
    pygame.draw.rect(WIN, "white", player)
    pygame.draw.rect(WIN, "grey", weapon)
    for obstacle in obstacle_list:
        pygame.draw.rect(WIN, "brown", obstacle.rect)
    for bullet in bullet_list:
        pygame.draw.rect(WIN, "yellow", bullet.rect)
    for enemy in enemy_list:
        pygame.draw.rect(WIN, "red", enemy.rect)

    pygame.display.update()


def generate_obstacles(min_enemy, max_enemy):
    obstacle_list = []
    total_obstacle = random.randint(min_enemy, max_enemy)
    for i in range(total_obstacle):
        obs_x = random.randint(0, s.WIDTH - s.BOX_WIDTH)
        obs_y = random.randint(0, s.HEIGHT - s.BOX_HEIGHT)
        obstacle = Obstacle(obs_x, obs_y, 1)
        obstacle_list.append(obstacle)
    return obstacle_list


def generate_enemies(min_enemy, max_enemy):
    enemy_list = []
    total_enemy = random.randint(min_enemy, max_enemy)
    for i in range(total_enemy):
        pos_x = random.randint(0, s.WIDTH - s.BOX_WIDTH)
        pos_y = random.randint(-20, 10)
        obstacle = Enemy(pos_x, pos_y, 1)
        enemy_list.append(obstacle)
    return enemy_list


def main():
    game_active = True
    clock = pygame.time.Clock()
    player = Player(s.WIDTH // 2 - s.PLAYER_WIDTH // 2, s.HEIGHT - s.PLAYER_HEIGHT, s.PLAYER_VEL)
    weapon = pygame.Rect(player.rect.x, player.rect.y, s.WEAPON_WIDTH, s.WEAPON_HEIGHT)
    bullet_list = []
    last_shot_time = time.time()

    obstacle_list = generate_obstacles(0, 0)
    enemy_list = generate_enemies(10, 10)

    while game_active:
        clock.tick(s.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT_____")
                game_active = False
                break
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player.rect.x - s.PLAYER_VEL >= 0:
            player.rect.x -= s.PLAYER_VEL
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player.rect.x + s.PLAYER_VEL <= s.WIDTH - s.PLAYER_WIDTH:
            player.rect.x += s.PLAYER_VEL
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and player.rect.y - s.PLAYER_VEL >= 0:
            player.rect.y -= s.PLAYER_VEL
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and player.rect.y + s.PLAYER_VEL <= s.HEIGHT - s.PLAYER_HEIGHT:
            player.rect.y += s.PLAYER_VEL
        weapon.x = player.rect.x
        weapon.y = player.rect.y
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and time.time() - last_shot_time > s.RATE_OF_FIRE_per_min:
            bullet_speed = s.BULLET_VEL
            bullet_velocity = calculate_bullet_velocity(
                (weapon.x + s.WEAPON_WIDTH // 2, weapon.y + s.WEAPON_HEIGHT // 2),
                (mouse_pos_x, mouse_pos_y), bullet_speed)
            bullet_angle = math.degrees(math.atan2(bullet_velocity[0], bullet_velocity[1]))
            bullet = Bullet(weapon.x + s.WEAPON_WIDTH // 2 - s.BULLET_WIDTH // 2, weapon.y, bullet_angle,
                            bullet_velocity)
            bullet_list.append(bullet)
            last_shot_time = time.time()

        check_bullet_obstacle_collision(bullet_list, obstacle_list)
        check_bullet_obstacle_collision(bullet_list, enemy_list)
        check_player_obstacle_collision(player, obstacle_list)
        check_player_enemy_collision(player, enemy_list)

        if player.current_health <= 0:
            time.sleep(3)
            print("Game Over")
            main()
        for enemy in enemy_list:
            enemy.move_towards_player(player.rect)
        for bullet in bullet_list:
            bullet.move()
            if bullet.rect.y < 0 or bullet.rect.x < 0 or bullet.rect.x > s.WIDTH or bullet.rect.y > s.HEIGHT:
                bullet_list.remove(bullet)
        if len(enemy_list) == 0:
            enemy_list = generate_enemies(10, 10)
        draw(player, weapon, bullet_list, obstacle_list, enemy_list)
    pygame.quit()


if __name__ == "__main__":
    main()
