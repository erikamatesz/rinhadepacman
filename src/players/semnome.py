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
import heapq

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha,
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class SemNome(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial
        # do seu Pac-Man na planilha.
        x = 9
        y = 21
        color = (175, 250, 29)  # Coloque aqui o código RGB do seu Pac-Man.
        super().__init__("SemNome", x, y, color)  # Atualize o nome dele.
        self.update_position()

    def move(self, pills):
        # Lembre-se que, além da variável pills, você tem acesso às variáveis globais MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------

        pos = [self.x,self.y]

        # Verificar se ainda há comidas no mapa
        if pills:
            # Encontre a comida mais próxima
            nearest_food = min(pills, key=lambda pill: self.manhattan_distance(pos, [pill.x, pill.y]))

            # Calcule o caminho até a comida mais próxima usando o A*
            path = self.astar(pos, [nearest_food.x, nearest_food.y], MAZE)

            # Se houver um caminho, mova Pacman para o próximo passo no caminho
            if path:
                next_step = path[0]  # Pegue a primeira posição do caminho gerado
                direction = [next_step[0] - pos[0], next_step[1] - pos[1]]  # Defina a direção com base no próximo passo

                # Atualize a posição de Pacman
                nextpos = [pos[0] + direction[0], pos[1] + direction[1]]
                row = nextpos[1]
                col = nextpos[0]

                # Verifique se a próxima posição é válida (não é uma parede)
                if 0 <= row < len(MAZE) and 0 <= col < len(MAZE[0]) and MAZE[row][col] != '#':
                    # Atualize a posição de Pacman de fato (não apenas a variável 'pos')
                    self.x = nextpos[0]
                    self.y = nextpos[1]
                    print(f"Pacman moved to {nextpos}")
                else:
                    print("Hit a wall or another Pacman, can't move!")

        else:
            print("No more food!")

        # ------------------------------ Final da sua implementação -----------------------------------------

        self.eat_pills(pills)  # Não apague!

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

    def manhattan_distance(self, start, goal):
        return abs(start[0] - goal[0]) + abs(start[1] - goal[1])

    #def euclidean_distance(self, start, goal):
    #    return math.sqrt((start[0] - goal[0]) ** 2 + (start[1] - goal[1]) ** 2)

    def astar(self, start, goal, maze):
        direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[tuple(start)] = None
        cost_so_far[tuple(start)] = 0

        while open_list:
            _, current = heapq.heappop(open_list)

            # Quando o Pacman alcançar o objetivo (comida)
            if current == goal:
                break

            for d in direction:
                next_pos = [current[0] + d[0], current[1] + d[1]]
                row, col = next_pos[1], next_pos[0]

                if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and maze[row][col] != '#':
                    new_cost = cost_so_far[tuple(current)] + 1
                    if tuple(next_pos) not in cost_so_far or new_cost < cost_so_far[tuple(next_pos)]:
                        cost_so_far[tuple(next_pos)] = new_cost
                        priority = new_cost + self.manhattan_distance(next_pos, goal)
                        heapq.heappush(open_list, (priority, next_pos))
                        came_from[tuple(next_pos)] = current

        # Verifique se um caminho foi encontrado
        if tuple(goal) not in came_from:
            print(f"No valid path found to {goal}")
            return []

        # Reconstruir o caminho
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[tuple(current)]
        path.reverse()
        return path
