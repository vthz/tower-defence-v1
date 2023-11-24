import pygame
from config import settings as s
import random

player_color_list = ["red", "green", "blue", "orange"]


class Player:
    def __init__(self, x, y, vel=s.PLAYER_VEL):
        self.rect = pygame.Rect(x, y, s.PLAYER_WIDTH, s.PLAYER_HEIGHT)
        self.vel = vel
        self.move = True
        self.current_health = 100
        self.player_color = player_color_list[random.randint(0, len(player_color_list)-1)]

    def move_player(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x - s.PLAYER_VEL >= 0:
            self.rect.x -= s.PLAYER_VEL
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x + s.PLAYER_VEL <= s.WIDTH - s.PLAYER_WIDTH:
            self.rect.x += s.PLAYER_VEL
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y - s.PLAYER_VEL >= 0:
            self.rect.y -= s.PLAYER_VEL
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y + s.PLAYER_VEL <= s.HEIGHT - s.PLAYER_HEIGHT:
            self.rect.y += s.PLAYER_VEL
