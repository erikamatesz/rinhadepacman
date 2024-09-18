from players.pacman import Pacman
from game.config import *
from queue import PriorityQueue

class Taz(Pacman):
    def __init__(self):
        x = 21
        y = 10
        color = (135, 71, 11)
        super().__init__("Taz", x, y, color)
        self.update_position()  # Atualiza a posição do Pac-Man após inicializar

    def move(self, pills):
        # Variáveis globais: MAZE, AGENTS_POSITIONS
        start = (self.x, self.y)  # Posição inicial do Pac-Man
        ghosts = [pos for name, pos in AGENTS_POSITIONS.items() if 'ghost' in name]  # Posições dos fantasmas
        pacman_positions = [pos for name, pos in AGENTS_POSITIONS.items() if 'pacman' in name and name != self.name]  # Posições dos outros Pac-Mans

        # Encontrar a pílula mais próxima usando A*
        target_pill = self.find_nearest_pill(pills, ghosts, pacman_positions)

        if target_pill:
            path = self.a_star(start, (target_pill.x, target_pill.y), ghosts, pacman_positions)  # Acessa as coordenadas da pílula
            print(f"Path found: {path}")  # Depuração: imprime o caminho encontrado
            
            if path and len(path) > 1:  # Certifica-se de que o caminho tenha pelo menos dois pontos
                next_move = path[1]  # Próximo passo no caminho
                if self.is_valid_move(next_move, ghosts, pacman_positions):  # Verifica se o movimento é válido
                    self.x, self.y = next_move  # Atualiza a posição do Pac-Man
                else:
                    print(f"Invalid move: {next_move}")  # Depuração: imprime movimento inválido
                
                # Verifica se o Pac-Man colidiu com algum fantasma
                if (self.x, self.y) in ghosts:
                    self.die()  # Método para tratar a morte do Pac-Man
            else:
                # Se o caminho não foi encontrado, permanece na posição atual
                self.x, self.y = start
        else:
            # Se não houver pílula, não se move
            print("No nearest pill found.")  # Depuração: imprime se não encontrar pílula

        self.eat_pills(pills)  # Não apague!

    def a_star(self, start, goal, ghosts, pacman_positions):
        # Implementação do algoritmo A* considerando fantasmas e outros Pac-Mans
        frontier = PriorityQueue()
        frontier.put((0, start))
        came_from = {start: None}
        cost_so_far = {start: 0}

        while not frontier.empty():
            _, current = frontier.get()

            if current == goal:
                break

            for next_pos in self.get_neighbors(current):
                if next_pos in ghosts or next_pos in pacman_positions:
                    continue  # Evita fantasmas e outros Pac-Mans
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.manhattan_distance(next_pos, goal)
                    frontier.put((priority, next_pos))
                    came_from[next_pos] = current

        # Reconstrói o caminho
        return self.reconstruct_path(came_from, start, goal)

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        if y > 0 and MAZE[y-1][x] != '#':  # Cima
            neighbors.append((x, y-1))
        if y < len(MAZE) - 1 and MAZE[y+1][x] != '#':  # Baixo
            neighbors.append((x, y+1))
        if x > 0 and MAZE[y][x-1] != '#':  # Esquerda
            neighbors.append((x-1, y))
        if x < len(MAZE[0]) - 1 and MAZE[y][x+1] != '#':  # Direita
            neighbors.append((x+1, y))
        return neighbors

    def manhattan_distance(self, a, b):
        # Heurística de distância de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, start, goal):
        # Reconstrói o caminho do Pac-Man até a pílula
        current = goal
        path = [current]
        while current != start:
            current = came_from.get(current)
            if current is None:
                return []  # Retorna caminho vazio se não for possível chegar ao objetivo
            path.append(current)
        path.reverse()
        return path

    def find_nearest_pill(self, pills, ghosts, pacman_positions):
        # Encontra a pílula mais próxima que não está bloqueada por fantasmas ou outros Pac-Mans
        min_distance = float('inf')
        nearest_pill = None
        for pill in pills:
            distance = self.manhattan_distance((self.x, self.y), (pill.x, pill.y))  # Acessa as coordenadas da pílula
            if distance < min_distance and (pill.x, pill.y) not in ghosts and (pill.x, pill.y) not in pacman_positions:
                min_distance = distance
                nearest_pill = pill
        return nearest_pill

    def is_valid_move(self, position, ghosts, pacman_positions):
        # Verifica se a posição é um movimento válido (não passa pelas paredes, não está ocupada por um fantasma ou outro Pac-Man)
        x, y = position
        if 0 <= y < len(MAZE) and 0 <= x < len(MAZE[0]) and MAZE[y][x] != '#' and position not in ghosts and position not in pacman_positions:
            return True
        return False

    def die(self):
        # Método para tratar a morte do Pac-Man
        print(f"{self.name} has been caught by a ghost!")  # Depuração: imprime que o Pac-Man morreu
        # Aqui você pode adicionar lógica adicional para a morte do Pac-Man, como reiniciar o jogo ou finalizar a partida.
        self.x, self.y = (-1, -1)  # Exemplo de reposicionamento fora do labirinto
        self.update_position()  # Atualiza a posição do Pac-Man para refletir a morte

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
