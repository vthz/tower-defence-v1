import pygame
from config import settings as s


class Obstacle:
    def __init__(self, x, y, model_id):
        self.rect = pygame.Rect(x, y, s.BOX_WIDTH, s.BOX_HEIGHT)
        self.model_id = model_id
        self.hit_points = 100
        self.destruction_points = 5
