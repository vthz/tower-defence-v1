import pygame
from config import settings as s
import math


class Enemy:
    def __init__(self, x, y, model_id, vel=s.ENEMY_VEL):
        self.rect = pygame.Rect(x, y, s.BOX_WIDTH, s.BOX_HEIGHT)
        self.model_id = model_id
        self.hit_points = 50
        self.vel = vel
        self.max_damage = 10
        self.destruction_points = 10

    def move_towards_player(self, player_rect):
        angle = math.atan2(player_rect.centery - self.rect.centery, player_rect.centerx - self.rect.centerx)
        vel_x = self.vel * math.cos(angle)
        vel_y = self.vel * math.sin(angle)
        self.rect.x += vel_x
        self.rect.y += vel_y
