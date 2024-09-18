
from players.pacman import Pacman
from game.config import *
import heapq
# import random

Directions = {
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP': (0, -1),
    'DOWN': (0, 1)
}


class Kawabanga(Pacman):
    def __init__(self):
        x = 21
        y = 27
        color = (77, 5, 20)
        super().__init__("Kawabanga", x, y, color)

        self.path = []

    def move(self, pills):
        start = (self.x, self.y)  # Posição atual do Pac-Man

        # if not pills:
        #     print("Nenhuma pílula restante. Movendo de forma aleatória.")
        #     self.random_move()
        #     return

        # Se não há caminho calculado, calcular um novo
        if not self.path:
            self.path = self.a_star(start, pills)

        if self.path:  # Se há um caminho calculado, mover para a próxima posição
            next_position = self.path[0]
            self.state = self.get_next_state(start, next_position)
            self.update_position_state_based()
            self.path.pop(0)

        self.eat_pills(pills)

    def a_star(self, start, pills):

        if not pills:
            return []

        nearest_pill = min(
            pills, key=lambda pill: self.manhattan_distance(start, (pill.x, pill.y)))
        nearest_pill_position = (nearest_pill.x, nearest_pill.y)

        # Esta lista armazena os nós a serem explorados, ordenados pelo custo estimado
        priority_list = []
        # "A função heappush() é usada para inserir um novo item em uma fila de prioridade (ou heap)""
        heapq.heappush(priority_list, (0, start, None))

        came_from = {}

        # custo acumulado
        g_score = {start: 0}

        # estimativa heurística da distância até a pílula
        f_score = {start: self.manhattan_distance(
            start, nearest_pill_position)}

        while priority_list:
            current_cost, current, current_parent = heapq.heappop(
                priority_list)

            if current == nearest_pill_position:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1 + \
                    self.get_ghost_penalty(neighbor, AGENTS_POSITIONS)
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + \
                        self.manhattan_distance(
                            neighbor, nearest_pill_position)
                    heapq.heappush(
                        priority_list, (f_score[neighbor], neighbor, current))

        return None

    def get_ghost_penalty(self, position, agents_positions):
        penalty = 0
        for agent_position in agents_positions.values():
            if agent_position != position:  # Evitar calcular a distância para si mesmo
                distance_to_agent = self.manhattan_distance(
                    position, agent_position)
                if distance_to_agent <= 2:
                    penalty += (4 - distance_to_agent) * 10
        return penalty

    def get_neighbors(self, position):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            new_x, new_y = position[0] + dx, position[1] + dy
            if 0 <= new_x < len(MAZE[0]) and 0 <= new_y < len(MAZE) and MAZE[new_y][new_x] != '#':
                neighbors.append((new_x, new_y))
        return neighbors

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def reconstruct_path(self, came_from, current):
        total_path = []
        while current in came_from:
            total_path.append(current)
            current = came_from[current]
        total_path.reverse()
        return total_path

    # def random_move(self):
    #     # Obter todos os vizinhos válidos para a posição atual
    #     start = (self.x, self.y)
    #     neighbors = self.get_neighbors(start)

    #     if neighbors:  # Se houver vizinhos válidos
    #         # Escolhe um vizinho aleatoriamente
    #         next_position = random.choice(neighbors)
    #         self.state = self.get_next_state(start, next_position)
    #         self.update_position_state_based()

    def get_next_state(self, start, next_position):
        # Determina a direção para a próxima posição no caminho
        direction = (next_position[0] - start[0], next_position[1] - start[1])
        for state, (dx, dy) in Directions.items():
            if direction == (dx, dy):
                return state
        return None

    def update_position_state_based(self):
        # Atualiza a posição do Pac-Man baseado na direção atual
        dx, dy = Directions.get(self.state, (0, 0))
        self.x += dx
        self.y += dy

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
