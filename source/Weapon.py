import pygame
from config import settings as s


class Weapon:
    def __init__(self, x, y, vel=s.PLAYER_VEL):
        self.rect = pygame.Rect(x, y, s.WEAPON_WIDTH, s.WEAPON_HEIGHT)
        self.vel = vel
