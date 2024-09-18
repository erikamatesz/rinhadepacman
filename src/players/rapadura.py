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

import heapq  # Necessário para a implementação do A*
from players.pacman import Pacman
from game.config import *


#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class Rapadura(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial 
        # do seu Pac-Man na planilha.
        x = 17
        y = 10
        color = (165, 51, 120) # Coloque aqui o código RGB do seu Pac-Man.
        super().__init__("Rapadura", x, y, color) # Atualize o nome dele.
        self.update_position()
    
    def move(self, pills):
        # Lembre-se que, além da variável pills, você tem acesso às variáveis globais MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------

        start=(self.x, self.y)
          
        # Defina o objetivo como a pílula mais próxima
        goal = self.find_closest_pill(pills)

        # Se houver uma pílula válida e o caminho for encontrado
        if goal:
            path = self.a_star(MAZE, start, goal)

            # Verifique se o caminho foi encontrado e se tem mais de 1 passo
            if path and len(path) > 1:
                next_move = path[1]  # O primeiro movimento do caminho
                self.x, self.y = next_move
            else:
                print(f"Não foi possível encontrar um caminho de {start} para {goal}")
        else:
            print("Nenhuma pílula encontrada ou caminho inválido.")

    # Atualize a posição e verifique pílulas
        
        # ------------------------------ Final da sua implementação -----------------------------------------

        self.eat_pills(pills) # Não apague!
    
    def find_closest_pill(self, pills):
        # Encontra a pílula mais próxima com base na distância de Manhattan
        min_distance = float('inf')
        closest_pill = None
        for pill in pills:
            dist = abs(self.x - pill.x) + abs(self.y - pill.y)
            if dist < min_distance:
                min_distance = dist
                closest_pill = (pill.x, pill.y)
        return closest_pill
    
    def a_star(self, maze, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while open_list:
            _, current = heapq.heappop(open_list)

            for next_move in self.get_neighbors(maze, current):
                # Adicionar uma penalidade se o próximo movimento estiver perto de um fantasma
                new_cost = cost_so_far[current] + 1 + self.ghost_penalty(next_move)  # Penalidade de fantasma

                if next_move not in cost_so_far or new_cost < cost_so_far[next_move]:
                    cost_so_far[next_move] = new_cost
                    priority = new_cost + self.heuristic(next_move, goal)
                    heapq.heappush(open_list, (priority, next_move))
                    came_from[next_move] = current

        if goal not in came_from:
            print(f"Nenhum caminho encontrado para {goal}")
            return []

        return self.reconstruct_path(came_from, start, goal)


    def get_neighbors(self, maze, current):
        # Retorna os vizinhos válidos (não paredes) ao redor da posição atual
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Direções: direita, baixo, esquerda, cima
        for direction in directions:
            neighbor = (current[0] + direction[0], current[1] + direction[1])
            if maze[neighbor[1]][neighbor[0]] != '#':  # Verifique se não é uma parede
                neighbors.append(neighbor)
        return neighbors

    def heuristic(self, a, b):
        # Função heurística: distância de Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    
    def ghost_penalty(self, position):
            # Função que penaliza áreas próximas de fantasmas
            penalty = 0
            for ghost_position in AGENTS_POSITIONS.values():
                # Calcule a distância de Manhattan entre o Pac-Man e o fantasma
                distance_to_ghost = abs(position[0] - ghost_position[0]) + abs(position[1] - ghost_position[1])

                # Se a posição estiver muito próxima de um fantasma, aplique uma penalidade
                if distance_to_ghost == 1:  # Fantasma ao lado
                    penalty += 10  # Penalidade alta para áreas adjacentes
                elif distance_to_ghost == 2:  # Fantasma a duas casas
                    penalty += 5  # Penalidade menor, mas ainda preocupante

            return penalty

    def reconstruct_path(self, came_from, start, goal):
        # Reconstrói o caminho desde o objetivo até a posição inicial
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = came_from[current]
        path.append(start)
        path.reverse()  # Inverte o caminho para ficar na ordem correta
        return path

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

