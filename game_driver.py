import math
import time
import random

import pygame
from config import settings as s

from source.Player import Player
from source.Weapon import Weapon
from source.Enemy import Enemy
from source.Bullet import Bullet
from source.Obstacle import Obstacle

pygame.font.init()

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
WIN_BG = pygame.transform.scale(pygame.image.load("assets/background/bg_black.png"), (s.WIDTH, s.HEIGHT))
HEART_ICON = pygame.transform.scale(pygame.image.load("assets/icons/heart_icon.png"), (20, 20))
FONT = pygame.font.SysFont("comicsans", 30)
pygame.display.set_caption("Wave Defence v1-18nov23")


class GameMechanics:
    def __init__(self):
        self.current_score = 0
        self.bullet_list = []
        self.last_shot_time = time.time()
        self.wave_count = 0

    def get_current_score(self):
        return self.current_score

    def bullet_logic(self, weapon):
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and time.time() - self.last_shot_time > s.RATE_OF_FIRE_per_min:
            bullet_speed = s.BULLET_VEL
            bullet_velocity = calculate_bullet_velocity(
                (weapon.rect.x + s.WEAPON_WIDTH // 2, weapon.rect.y + s.WEAPON_HEIGHT // 2),
                (mouse_pos_x, mouse_pos_y), bullet_speed)
            bullet_angle = math.degrees(math.atan2(bullet_velocity[0], bullet_velocity[1]))
            bullet = Bullet(weapon.rect.x + s.WEAPON_WIDTH // 2 - s.BULLET_WIDTH // 2, weapon.rect.y, bullet_angle,
                            bullet_velocity)
            self.bullet_list.append(bullet)
            self.last_shot_time = time.time()


def calculate_bullet_velocity(player_pos, mouse_pos, bullet_speed):
    angle = math.atan2(mouse_pos[1] - player_pos[1], mouse_pos[0] - player_pos[0])
    vel_x = bullet_speed * math.cos(angle)
    vel_y = bullet_speed * math.sin(angle)
    return vel_x, vel_y


def check_bullet_obstacle_collision(bullets, obstacles, gameObj):  # this function being used to determine
    for bullet in bullets:
        for obstacle in obstacles:
            if bullet.rect.colliderect(obstacle.rect):
                obstacle.hit_points -= bullet.total_damage
                if obstacle.hit_points <= 0:
                    obstacles.remove(obstacle)
                    gameObj.current_score += obstacle.destruction_points
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


def draw(player, weapon, bullet_list, obstacle_list, enemy_list, gameObj):
    WIN.blit(WIN_BG, (0, 0))
    score_text = FONT.render(f"$:{gameObj.current_score}", 1, "white")
    WIN.blit(score_text, (10, 10))
    # enemy_count_text = FONT.render(f"Enemy:{len(enemy_list)}  Wave:{gameObj.wave_count}", 1, "white")
    # WIN.blit(enemy_count_text, ((s.WIDTH // 2 - enemy_count_text.get_width() // 2), 10))
    health_text = FONT.render(f"{max(0, player.current_health)}", 1, "white")
    WIN.blit(health_text, (s.WIDTH - len(str(player.current_health) * 20), 10))
    WIN.blit(HEART_ICON, (s.WIDTH - len(str(player.current_health) * 20) - 25, 25))
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
    weapon = Weapon(player.rect.x, player.rect.y, player.vel)
    min_enemy, max_enemy = 10, 10
    obstacle_list = generate_obstacles(0, 0)
    enemy_list = generate_enemies(min_enemy, max_enemy)

    gameObj = GameMechanics()

    while game_active:
        clock.tick(s.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("QUIT_____")
                game_active = False
                break
        player.move_player()
        weapon.rect.x = player.rect.x
        weapon.rect.y = player.rect.y
        gameObj.bullet_logic(weapon)

        check_bullet_obstacle_collision(gameObj.bullet_list, obstacle_list, gameObj)
        check_bullet_obstacle_collision(gameObj.bullet_list, enemy_list, gameObj)
        check_player_obstacle_collision(player, obstacle_list)
        check_player_enemy_collision(player, enemy_list)

        for enemy in enemy_list:
            enemy.move_towards_player(player.rect)
        for bullet in gameObj.bullet_list:
            bullet.move()
            if bullet.rect.y < 0 or bullet.rect.x < 0 or bullet.rect.x > s.WIDTH or bullet.rect.y > s.HEIGHT:
                gameObj.bullet_list.remove(bullet)
        if len(enemy_list) == 0:
            enemy_list = generate_enemies(min_enemy, max_enemy)
            gameObj.wave_count += 1
        draw(player, weapon, gameObj.bullet_list, obstacle_list, enemy_list, gameObj)
        if player.current_health <= 0:
            time.sleep(3)
            print("Game Over")
            main()
    pygame.quit()


if __name__ == "__main__":
    main()
