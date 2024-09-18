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
import random

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#
import heapq  # Adiciona a importação do heapq para usar a fila de prioridade

class Nielsen(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial 
        # do seu Pac-Man na planilha.
        x = 21
        y = 21
        color = (51, 0, 169) # Coloque aqui o código RGB do seu Pac-Man.
        super().__init__("Nielsen", x, y, color) # Atualize o nome dele.
        self.update_position()
    
    def move(self, pills):
        # Lembre-se que, além da variável pills, você tem acesso às variáveis globais MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------
        # Obter a posição atual do Pac-Man
        def distancia_manhattan(p1, p2):
            return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

        # Função A* para encontrar o caminho até o destino
        def a_star(inicio, objetivo):
            # Definindo a lista de movimentos possíveis (cima, baixo, direita, esquerda)
            movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

            # Definindo a fila de prioridade para A*
            open_list = []
            heapq.heappush(open_list, (0, inicio))
            
            # Dicionários para armazenar o custo e o caminho
            g_costs = {inicio: 0}
            came_from = {inicio: None}
            
            while open_list:
                _, atual = heapq.heappop(open_list)

                # Se chegou ao objetivo, reconstrói o caminho
                if atual == objetivo:
                    caminho = []
                    while came_from[atual] is not None:
                        caminho.append(atual)
                        atual = came_from[atual]
                    caminho.reverse()
                    return caminho

                # Explora os vizinhos
                for dx, dy in movimentos:
                    vizinho = (atual[0] + dx, atual[1] + dy)

                    # Verifica se o vizinho está dentro dos limites do labirinto e não é uma parede
                    if 0 <= vizinho[0] < len(MAZE) and 0 <= vizinho[1] < len(MAZE[0]) and MAZE[vizinho[0]][vizinho[1]] != 'WALL':
                        novo_custo = g_costs[atual] + 1
                        
                        # Se o vizinho não estiver no g_costs ou encontrou um caminho mais curto
                        if vizinho not in g_costs or novo_custo < g_costs[vizinho]:
                            g_costs[vizinho] = novo_custo
                            prioridade = novo_custo + distancia_manhattan(vizinho, objetivo)
                            heapq.heappush(open_list, (prioridade, vizinho))
                            came_from[vizinho] = atual

            return []  # Retorna uma lista vazia se não houver caminho

        # Encontrar a pílula mais próxima
        if pills:
            p_pill = min(pills, key=lambda p: distancia_manhattan((self.x, self.y), (p.x, p.y)))
        else:
            p_pill = None

        # Usar A* para encontrar o caminho até a pílula mais próxima
        if p_pill:
            caminho = a_star((self.x, self.y), (p_pill.x, p_pill.y))
            
            # Executar o primeiro movimento do caminho
            if caminho:
                proximo_passo = caminho[0]
                self.x, self.y = proximo_passo

        # Atualizar a posição
        self.update_position()

        # ------------------------------ Final da sua implementação -----------------------------------------

        self.eat_pills(pills) # Não apague!

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
