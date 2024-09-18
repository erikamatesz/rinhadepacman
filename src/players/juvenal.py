# 
# INFORMAÇÕES GERAIS
#
# 1 - Você tem acesso à variável global MAZE (estática) que é o labirinto.
# 2 - Você tem acesso à variável global AGENTS_POSITIONS (dinâmica) que mostra
#     as posições dos fantasmas e de cada Pac-Man. 
# 3 - Este arquivo nomedoseuagente.py é onde você vai inserir o seu código. 
#     Você NÃO pode inserir ou alterar código fora dele.
# 4 - Não altere os imports existentes. 
# 5 - Se precisar adicionar imports, adicione somente na classe do seu agente e, 
#     caso o seu import seja de uma dependência que precisa ser instalada, 
#     adicione essa dependência no arquivo requirements.txt e rode 
#     pip install -r requirements.txt
#

from players.pacman import Pacman
from game.config import *
from collections import deque

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

from collections import deque

class Juvenal(Pacman):
    def __init__(self):
        x = 28
        y = 22
        color = (255, 100, 100)
        super().__init__("Juvenal", x, y, color)
        self.update_position()

    def bfs(self, target, occupied_positions):
        queue = deque([(self.x, self.y, [])])
        visited = set((self.x, self.y))

        while queue:
            x, y, path = queue.popleft()

            if (x, y) == target:
                return path

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < len(MAZE[0]) and 0 <= ny < len(MAZE) and MAZE[ny][nx] != '#' and (nx, ny) not in visited and (nx, ny) not in occupied_positions:
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(dx, dy)]))

        return None
    
    def move(self, pills):
        ghost_names = ["Blinky", "Inky", "Pinky", "Clyde"]
        occupied_positions = [pos for agent, pos in AGENTS_POSITIONS.items() if agent in ghost_names]
        
        # Check the distance to the nearest ghost
        nearest_ghost_distance = float('inf')
        nearest_ghost_position = None
        for ghost_pos in occupied_positions:
            dist = abs(self.x - ghost_pos[0]) + abs(self.y - ghost_pos[1])
            if dist < nearest_ghost_distance:
                nearest_ghost_distance = dist
                nearest_ghost_position = ghost_pos

        # If a ghost is too close, move away from it
        if nearest_ghost_distance < 3:  # Define a threshold for "too close"
            # Calculate a position away from the ghost
            escape_path = self.bfs(self.escape_from_ghost(nearest_ghost_position), occupied_positions)
            if escape_path:
                move = escape_path[0]
                self.x += move[0]
                self.y += move[1]
        else:
            # Find the closest pill if no ghost is too close
            closest_pill = None
            min_dist = float('inf')
            for pill in pills:
                pill_x, pill_y = pill.x, pill.y
                dist = abs(self.x - pill_x) + abs(self.y - pill_y)
                if dist < min_dist:
                    closest_pill = (pill_x, pill_y)
                    min_dist = dist

            # Perform BFS to find the shortest path to the closest pill
            if closest_pill:
                path = self.bfs(closest_pill, occupied_positions)
                if path:
                    move = path[0]
                    self.x += move[0]
                    self.y += move[1]

        self.update_position()
        self.eat_pills(pills)

    def escape_from_ghost(self, ghost_pos):
        # Determine an escape position that is farther away from the ghost
        ghost_x, ghost_y = ghost_pos
        # Return a position that is a few steps away from the ghost
        escape_positions = [
            (ghost_x - 2, ghost_y),  # Move left
            (ghost_x + 2, ghost_y),  # Move right
            (ghost_x, ghost_y - 2),  # Move up
            (ghost_x, ghost_y + 2)   # Move down
        ]
        # Choose the first valid escape position
        for pos in escape_positions:
            if 0 <= pos[0] < len(MAZE[0]) and 0 <= pos[1] < len(MAZE) and MAZE[pos[1]][pos[0]] != '#':
                return pos
        return ghost_pos  # Fallback to the ghost's position if no valid escape found

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

