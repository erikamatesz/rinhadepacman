from players.pacman import Pacman
from game.config import *
import random
import heapq
import math

class Lups(Pacman):
    def __init__(self):
        x = 15
        y = 10
        # Cores do Fluminense: verde, branco e grená
        color = (118, 0, 0)  # Grená para destaque
        super().__init__("Lups", x, y, color)
        self.update_position()

    def move(self, pills):
        best_move = self.a_star_search(pills)
        if best_move:
            self.x, self.y = best_move

        # Comer pílulas
        self.eat_pills(pills)

    def a_star_search(self, pills):
        start = (self.x, self.y)
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, pills)}

        while open_set:
            current = heapq.heappop(open_set)[1]

            if self.is_near_pill(current, pills):
                return current

            for direction, (dx, dy) in self.get_directions().items():
                neighbor = (current[0] + dx, current[1] + dy)

                if self.is_valid_move(neighbor):
                    tentative_g_score = g_score[current] + 1

                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score[neighbor] = tentative_g_score + self.heuristic(neighbor, pills)

                        if neighbor not in [i[1] for i in open_set]:
                            heapq.heappush(open_set, (f_score[neighbor], neighbor))

        return None

    def heuristic(self, pos, pills):
        # Filtra pílulas que não foram comidas
        available_pills = [pill for pill in pills if not pill.eaten]
        
        # Verifica se há pílulas disponíveis
        if not available_pills:
            return float('inf')  # Retorna infinito se não houver pílulas

        # Distância euclidiana mínima para a pílula mais próxima
        return min(math.sqrt((pos[0] - pill.x) ** 2 + (pos[1] - pill.y) ** 2) for pill in available_pills)

    def is_near_pill(self, pos, pills):
        return any(pos == (pill.x, pill.y) for pill in pills if not pill.eaten)

    def is_valid_move(self, pos):
        max_x = len(MAZE[0]) - 1
        max_y = len(MAZE) - 1
        return (0 <= pos[0] <= max_x and 0 <= pos[1] <= max_y and MAZE[pos[1]][pos[0]] != '#')

    def get_directions(self):
        return {
            'left': (-1, 0),
            'right': (1, 0),
            'up': (0, -1),
            'down': (0, 1)
        }

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

# Função de distância euclidiana
def euclidean_dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
