import pygame
from config import settings as s
import math
import random

enemy_model_ids = [1, 2, 3, 4, 5]
enemy_characteristics = {1: [20, 5, 5, 5, 10],
                         2: [10, 4, 10, 10, 10],
                         3: [50, 3, 20, 10, 15],
                         4: [25, 2, 20, 10, 15],
                         5: [100, 1, 50, 50, 30]}


# enemy {model_id:[hit_points, velocity, damage, points_earned, length]}

class Enemy:
    def __init__(self, x, y):
        self.model_id = enemy_model_ids[random.randint(0, len(enemy_model_ids) - 1)]
        self.hit_points = enemy_characteristics[self.model_id][0]
        self.vel = enemy_characteristics[self.model_id][1]
        self.max_damage = enemy_characteristics[self.model_id][2]
        self.destruction_points = enemy_characteristics[self.model_id][3]
        self.rect = pygame.Rect(x, y, enemy_characteristics[self.model_id][4], enemy_characteristics[self.model_id][4])

    def move_towards_player(self, player_rect):
        angle = math.atan2(player_rect.centery - self.rect.centery, player_rect.centerx - self.rect.centerx)
        vel_x = self.vel * math.cos(angle)
        vel_y = self.vel * math.sin(angle)
        self.rect.x += vel_x
        self.rect.y += vel_y
