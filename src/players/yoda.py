
from players.pacman import Pacman
from game.config import *
import math
import heapq

DIRECTIONS = {
    'LEFT': (-1, 0),
    'RIGHT': (1, 0),
    'UP': (0, -1),
    'DOWN': (0, 1)
}

class Yoda(Pacman):
    def __init__(self):
        x = 1
        y = 5
        color = (0, 128, 0)
        super().__init__("Yoda", x, y, color)
        self.update_position()
        self.move_count = 0
        self.last_positions = []
        self.path_to_pill = []
        self.first_target_reached = False
        self.state = 'RIGHT'

    def move(self, pills):
        start = (self.x, self.y)
        self.move_count += 1
        self.last_positions.append(start)
        if len(self.last_positions) > 5:
            self.last_positions.pop(0)

        if not self.first_target_reached:
            target = (14, 5)
            if not self.path_to_pill or self.reached_target(target):
                self.path_to_pill = self.a_star(start, target)
            if self.reached_target(target):
                self.first_target_reached = True
                self.path_to_pill = []
        else:
            if not self.path_to_pill or self.reached_target(self.path_to_pill[-1]) or self.ghost_in_path():
                self.path_to_pill = self.a_star_to_pill_safe(start, pills)

            if self.path_to_pill:
                next_position = self.path_to_pill.pop(0)
                self.state = self.get_next_state(start, next_position)

        self.update_position_state_based()
        self.eat_pills(pills)

    def a_star(self, start, target):
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.manhattan_distance(start, target)}

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == target:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = g_score[neighbor] + self.manhattan_distance(neighbor, target)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

        return []

    def a_star_to_pill_safe(self, start, pills):
        available_pills = [pill for pill in pills if not pill.eaten]
        safe_paths = []

        for pill in available_pills:
            path = self.a_star(start, (pill.x, pill.y))
            if not self.ghost_in_path(path):
                safe_paths.append((path, pill))

        if safe_paths:
            best_path, _ = min(safe_paths, key=lambda item: len(item[0]))  # Escolhe o caminho mais curto seguro
            return best_path
        return []

    def ghost_in_path(self, path=None):
        if path is None:
            path = self.path_to_pill
        for position in path:
            if self.is_near_ghost(position):
                return True
        return False

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        total_path.reverse()
        return total_path

    def is_near_ghost(self, position):
        ghost_names = ["Inky", "Clyde", "Blinky", "Pinky"]
        for ghost_name in ghost_names:
            if ghost_name in AGENTS_POSITIONS:
                ghost_position = AGENTS_POSITIONS[ghost_name]
                if self.manhattan_distance(position, ghost_position) <= 2:
                    return True
        return False

    def get_next_state(self, start, next_position):
        direction = (next_position[0] - start[0], next_position[1] - start[1])
        for state, (dx, dy) in DIRECTIONS.items():
            if direction == (dx, dy):
                return state
        if self.path_to_pill:
            next_position = self.path_to_pill.pop(0)
            return self.get_next_state(start, next_position)
        else:
            self.path_to_pill = self.a_star_to_pill_safe(start, AGENTS_POSITIONS.get('pills', []))
            if self.path_to_pill:
                next_position = self.path_to_pill.pop(0)
                return self.get_next_state(start, next_position)
        return 'RIGHT'

    def update_position_state_based(self):
        if not hasattr(self, 'state'):
            self.state = 'RIGHT'
        dx, dy = DIRECTIONS.get(self.state, (0, 0))
        if self.is_valid_position((self.x + dx, self.y + dy)):
            self.x += dx
            self.y += dy

    def get_neighbors(self, position):
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dx, dy in directions:
            new_x, new_y = position[0] + dx, position[1] + dy
            if self.is_valid_position((new_x, new_y)):
                neighbors.append((new_x, new_y))
        return neighbors

    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def is_valid_position(self, position):
        new_x, new_y = position
        return 0 <= new_x < len(MAZE[0]) and 0 <= new_y < len(MAZE) and MAZE[new_y][new_x] != '#'


    def reached_target(self, target):
        return (self.x, self.y) == target


    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

