import pygame
import random
from game.config import *

class Ghost:
    def __init__(self, x, y, name, color, speed=1):
        self.x = x
        self.y = y
        self.name = name
        self.color = color
        self.speed = speed
        self.update_position()

    def move(self, target):
        max_x = len(MAZE[0]) - 1
        max_y = len(MAZE) - 1

        directions = []
        if self.x > 0 and MAZE[self.y][self.x - 1] != '#':  # esquerda
            directions.append((-1, 0))
        if self.x < max_x and MAZE[self.y][self.x + 1] != '#':  # direita
            directions.append((1, 0))
        if self.y > 0 and MAZE[self.y - 1][self.x] != '#':  # cima
            directions.append((0, -1))
        if self.y < max_y and MAZE[self.y + 1][self.x] != '#':  # baixo
            directions.append((0, 1))

        if directions:
            move_x, move_y = random.choice(directions)

            move_x *= self.speed
            move_y *= self.speed

            new_x = int(self.x + move_x)
            new_y = int(self.y + move_y)

            # garante que só se move em espaços válidos
            if 0 <= new_x <= max_x and 0 <= new_y <= max_y and MAZE[new_y][new_x] != '#':
                self.x = new_x
                self.y = new_y
            else:
                print(f"[ATENÇÃO] {self.name} está fora dos limites em ({new_x}, {new_y})!")
        else:
            print(f"[ATENÇÃO] Sem movimentos válidos para {self.name} em ({self.x}, {self.y})!")

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    def check_collision(self, pacman):
        return self.x == pacman.x and self.y == pacman.y

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
        