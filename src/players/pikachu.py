from players.pacman import Pacman
from game.config import *
import heapq

class Pikachu(Pacman):
    def __init__(self):
        x = 21
        y = 14
        color = (255, 255, 0)
        super().__init__("Pikachu", x, y, color)
        self.update_position()
    
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def neighbors(self, position):
        x, y = position
        neighbors = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        return [(nx, ny) for nx, ny in neighbors if MAZE[ny][nx] == '.']

    def a_star(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == goal:
                break

            for next in self.neighbors(current):
                new_cost = cost_so_far[current] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current

        if goal not in came_from:
            return None
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        return path

    def move(self, pills):
        remaining_pills = [(pill.x, pill.y) for pill in pills if not pill.eaten]

        if remaining_pills:
            closest_pill = min(remaining_pills, key=lambda pill: self.heuristic((self.x, self.y), pill))
            path = self.a_star((self.x, self.y), closest_pill)

            if path:
                next_move = path[0]
                self.x, self.y = next_move

        self.eat_pills(pills)
    
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
