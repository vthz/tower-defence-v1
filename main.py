import pygame
import settings

WIN = pygame.display.set_mode(settings.WIDTH, settings.HEIGHT)
pygame.display.set_caption("Project 1")


def main():
    game_active = True
    while game_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
                break
    pygame.quit()
