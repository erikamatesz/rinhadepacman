import pygame
from game.config import *

class Pill:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.eaten = False

    def draw(self, screen):
        if not self.eaten:
            pygame.draw.circle(screen, WHITE, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 6)

    def is_eaten(self, pacman):
        if (self.x == pacman.x and self.y == pacman.y):
            self.eaten = True
            return True
        return False
