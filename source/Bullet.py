import pygame
from config import settings as s


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
