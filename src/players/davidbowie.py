from players.pacman import Pacman
from game.config import *
import random

class DavidBowie(Pacman):
    def __init__(self):
        x = 39
        y = 10
        color = (250, 128, 114)
        super().__init__("David Bowie", x, y, color)
    
    def move(self, maze, pills):
        possible_moves = []
        if self.x > 0 and maze[self.y][self.x - 1] != '#':
            possible_moves.append((-1, 0))
        if self.x < len(maze[0]) - 1 and maze[self.y][self.x + 1] != '#':
            possible_moves.append((1, 0))
        if self.y > 0 and maze[self.y - 1][self.x] != '#':
            possible_moves.append((0, -1))
        if self.y < len(maze) - 1 and maze[self.y + 1][self.x] != '#':
            possible_moves.append((0, 1))
        
        if possible_moves:
            move = random.choice(possible_moves)
            self.x += move[0]
            self.y += move[1]

        self.eat_pills(pills)
