import pygame
from config import settings as s

WIN = pygame.display.set_mode((s.WIDTH, s.HEIGHT))
WIN_BG = pygame.transform.scale(pygame.image.load("assets/background/bg_black.png"), (s.WIDTH, s.HEIGHT))
pygame.display.set_caption("Project 1")


def draw(player, weapon, bullet_list):
    WIN.blit(WIN_BG, (0, 0))
    pygame.draw.rect(WIN, "red", player)
    pygame.draw.rect(WIN, "white", weapon)
    pygame.display.update()


def main():
    game_active = True
    clock = pygame.time.Clock()
    player = pygame.Rect(s.WIDTH // 2 - s.PLAYER_WIDTH // 2, s.HEIGHT - s.PLAYER_HEIGHT, s.PLAYER_WIDTH,
                         s.PLAYER_HEIGHT)
    weapon = pygame.Rect(player.x, player.y, s.WEAPON_WIDTH, s.WEAPON_HEIGHT)

    while game_active:
        clock.tick(s.FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                break
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - s.PLAYER_VEL >= 0:
            player.x -= s.PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + s.PLAYER_VEL <= s.WIDTH - s.PLAYER_WIDTH:
            player.x += s.PLAYER_VEL
        if keys[pygame.K_UP] and player.y - s.PLAYER_VEL >= 0:
            player.y -= s.PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + s.PLAYER_VEL <= s.HEIGHT - s.PLAYER_HEIGHT:
            player.y += s.PLAYER_VEL
        mouse_pos_x, mouse_pos_y = pygame.mouse.get_pos()
        print(mouse_pos_x, mouse_pos_y)
        draw(player, weapon, 0)
    pygame.quit()


if __name__ == "__main__":
    main()
