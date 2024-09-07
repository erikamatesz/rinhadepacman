import pygame
from game.config import *

class Pacman:
    def __init__(self, name="Pac-Man", x=0, y=0, color=(255, 255, 0)):
        self.name = name
        self.x = x
        self.y = y
        self.color = color
        self.score = 0
        self.alive = True
    
    def draw(self, screen):
        if self.alive:
            pygame.draw.circle(screen, self.color, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

    def eat_pills(self, pills):
        if self.alive:
            for pill in pills[:]:
                if pill.is_eaten(self):
                    pills.remove(pill)
                    self.score += 1

    def print_score(self):
        if self.alive:
            print(f"{self.name} comeu mais uma pílula e tem {self.score} no total \o/")
