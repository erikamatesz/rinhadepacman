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
from game.pill import Pill
import random
import heapq

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class Neo(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial 
        # do seu Pac-Man na planilha.
        x = 14
        y = 5
        color = (146, 95, 26) # Coloque aqui o código RGB do seu Pac-Man.
        super().__init__("Neo", x, y, color) # Atualize o nome dele.
        self.update_position()

    def move(self, pills):
        # Lembre-se que, além da variável pills, você tem acesso às variáveis globais MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------
        # pill[y, x]

        closest_biscuit = find_closest_biscuit(self, pills)
        
        if closest_biscuit:
            path = a_star_search((self.x, self.y), (closest_biscuit.x, closest_biscuit.y))

            if path:
                for x, y in path:
                    self.x = x
                    self.y = y

        self.eat_pills(pills) # Não apague!

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

# Função para encontrar o biscoito mais próximo
def find_closest_biscuit(self, biscuits):
    closest_biscuit = None
    min_distance = float('inf')
    for biscuit in biscuits:
        distance = abs(self.x - biscuit.x) + abs(self.y - biscuit.y)
        if distance < min_distance:
            min_distance = distance
            closest_biscuit = biscuit
    return closest_biscuit

# # Função heurística para o algoritmo A*
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# # Função para encontrar o caminho usando A*
def a_star_search(start, goal):
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            tentative_g_score = gscore[current] + 1
            if 0 <= neighbor[0] < len(MAZE[0]) and 0 <= neighbor[1] < len(MAZE):
                if MAZE[neighbor[1]][neighbor[0]] == "#":
                    continue
            else:
                continue

            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False