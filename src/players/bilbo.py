from collections import deque
from players.pacman import Pacman
from game.config import *

class Bilbo(Pacman):
    def __init__(self):
        x = 20
        y = 13
        color = (250, 128, 114)
        super().__init__("Bilbo", x, y, color)
        self.update_position()

    def bfs(self, target, occupied_positions):
        """Perform BFS to find the shortest path to the target, avoiding occupied positions."""
        queue = deque([(self.x, self.y, [])])  # Queue contains tuples (x, y, path)
        visited = set((self.x, self.y))  # Keep track of visited nodes

        while queue:
            x, y, path = queue.popleft()

            # Check if we reached the target
            if (x, y) == target:
                return path  # Return the path to the target

            # Explore possible moves (left, right, up, down)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                # Make sure the move is within bounds, not a wall, and not an occupied position
                if 0 <= nx < len(MAZE[0]) and 0 <= ny < len(MAZE) and MAZE[ny][nx] != '#' and (nx, ny) not in visited and (nx, ny) not in occupied_positions:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(dx, dy)]))  # Append the new move to the path

        return None  # No path found

    # def move(self, pills):
    #     # Get ghost positions to avoid
    #     ghost_names = ["Blinky", "Inky", "Pinky", "Clyde"]
    #     occupied_positions = [pos for agent, pos in AGENTS_POSITIONS.items() if agent in ghost_names]

    #     # Find the closest pill
    #     closest_pill = None
    #     min_dist = float('inf')
    #     for pill in pills:
    #         dist = abs(self.x - pill[0]) + abs(self.y - pill[1])  # Manhattan distance
    #         if dist < min_dist:
    #             closest_pill = pill
    #             min_dist = dist

    #     # Perform BFS to find the shortest path to the closest pill while avoiding ghosts
    #     if closest_pill:
    #         path = self.bfs(closest_pill, occupied_positions)
    #         if path:
    #             # Move according to the first step in the BFS path
    #             move = path[0]
    #             self.x += move[0]
    #             self.y += move[1]

    #     # Update the agent's position in the global AGENTS_POSITIONS dictionary
    #     self.update_position()

    #     # Eat the pill if David Bowie is on it
    #     self.eat_pills(pills)

    def move(self, pills):
        # Get ghost positions to avoid
        ghost_names = ["Blinky", "Inky", "Pinky", "Clyde"]
        occupied_positions = [pos for agent, pos in AGENTS_POSITIONS.items() if agent in ghost_names]

        # Find the closest pill
        closest_pill = None
        min_dist = float('inf')
        for pill in pills:
            # Assuming pill has attributes x and y for coordinates
            pill_x, pill_y = pill.x, pill.y
            dist = abs(self.x - pill_x) + abs(self.y - pill_y)  # Manhattan distance
            if dist < min_dist:
                closest_pill = (pill_x, pill_y)
                min_dist = dist

        # Perform BFS to find the shortest path to the closest pill while avoiding ghosts
        if closest_pill:
            path = self.bfs(closest_pill, occupied_positions)
            if path:
                # Move according to the first step in the BFS path
                move = path[0]
                self.x += move[0]
                self.y += move[1]

        # Update the agent's position in the global AGENTS_POSITIONS dictionary
        self.update_position()

        # Eat the pill if David Bowie is on it
        self.eat_pills(pills)


    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
