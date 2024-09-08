from players.pacman import Pacman
from game.config import *
import random

class FreddieMercury(Pacman):
    def __init__(self):
        x = 2
        y = 8
        color = (169, 169, 169)
        super().__init__("Freddie Mercury", x, y, color)
        self.update_position()
    
    def move(self, pills):
        possible_moves = []
        if self.x > 0 and MAZE[self.y][self.x - 1] != '#':
            possible_moves.append((-1, 0))
        if self.x < len(MAZE[0]) - 1 and MAZE[self.y][self.x + 1] != '#':
            possible_moves.append((1, 0))
        if self.y > 0 and MAZE[self.y - 1][self.x] != '#':
            possible_moves.append((0, -1))
        if self.y < len(MAZE) - 1 and MAZE[self.y + 1][self.x] != '#':
            possible_moves.append((0, 1))
        
        if possible_moves:
            move = random.choice(possible_moves)
            self.x += move[0]
            self.y += move[1]

        self.eat_pills(pills)

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
        