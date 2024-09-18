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

from players.pacman import Pacman
from game.config import *

# Import manual (exclusivo deste arquivo)
# Não foi necessário baixar nenhuma dependência, o HEAPQ já é nativo do python

import heapq

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha,
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class Stitch(Pacman):

    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial
        # do seu Pac-Man na planilha.
        x = 24
        y = 10
        color = (52, 161, 235) # Coloque aqui o código RGB do seu Pac-Man.

        self.path = []

        super().__init__("Stitch", x, y, color) # Atualize o nome dele.
        self.update_position()

        # --------------------------------------------------------------------------
        """
        Firula de implementação, para ignorar as posições iniciais dos jogadores (e armazenar).
        Estava tendo problema com o Pacman travando nos cantos e em posições aleatórias (onde era a posição inicial de cada jogador).
        """

        # Lista de posições ignoradas
        ignored_positions_fantasma = {
            "FANTASMA_1": (29, 39),
            "FANTASMA_1_1": (39, 29),
            "FANTASMA_2": (1, 1),
            "FANTASMA_3": (1, 39),
            "FANTASMA_3_1": (39, 1),
            "FANTASMA_4": (29, 1),
            "FANTASMA_4_1": (1, 29),
        }

        # Posições adicionais a serem ignoradas
        additional_ignored_positions = list(AGENTS_POSITIONS.values())
        # Combina as duas listas de posições ignoradas
        self.all_ignored_positions = list(ignored_positions_fantasma.values()) + additional_ignored_positions

        # print(self.pills)

    def move(self, pills):

        """
        Heuristica escolhida: Distância de Manhattan.
        """
        def heuristic(a, b):
            # Distância de Manhattan
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        """
        Verifica se a posição que ele QUER ir (adjacente) está, ou não, ocupada
        """
        def is_occupied(position):
            # Verifica se a posição está ocupada por outros Pacmans ou fantasmas, exceto os ignorados
            if position in list(AGENTS_POSITIONS.values()) and position != (self.x, self.y):

                # Ignora as posições delimitadas anteriormente
                if position not in self.all_ignored_positions:
                    # print(f"Posição ocupada por outro agente em {position}.")
                    return True

        """
        Implementa o algorítimo A* de busca
        """
        def a_star(start, goal):
            open_set = []
            heapq.heappush(open_set, (0 + heuristic(start, goal), 0, start))
            came_from = {}
            g_score = {start: 0}
            f_score = {start: heuristic(start, goal)}

            while open_set:
                _, current_g, current = heapq.heappop(open_set)

                if current == goal:
                    path = []
                    while current in came_from:
                        path.append(current)
                        current = came_from[current]
                    path.reverse()
                    return path

                # Mágica acontecendo!
                for move in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    neighbor = (current[0] + move[0], current[1] + move[1])
                    if 0 <= neighbor[0] < len(MAZE[0]) and 0 <= neighbor[1] < len(MAZE):

                        # Se o vizinho não for uma parede, e não estiver ocupado, IR PARA
                        if MAZE[neighbor[1]][neighbor[0]] != '#' and not is_occupied(neighbor):
                            # Calcula a "custo do caminho" até o vizinho.
                            tentative_g_score = g_score[current] + 1

                            """
                            Verifica se esse caminho para o vizinho é melhor do que qualquer caminho anterior.
                            Duas opções: OU NÃO VISITADO anteriormente, ou VISITADO ANTERIORMENTE
                                - Se NÃO VISITADO, adiciona na busca
                                - Se VISITADO, compara com outros para ver se é mais "barato" 
                            """
                            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                                came_from[neighbor] = current

                                # Atualiza o custo de movimento acumulado até o vizinho.
                                g_score[neighbor] = tentative_g_score
                                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)

                                # Adiciona o vizinho à lista de nós a serem explorados desde que ainda não tenha sido adicionado.
                                if neighbor not in [i[2] for i in open_set]:
                                    # Insere o vizinho no open_set. O nó com o menor valor de g_score será o próximo a ser expandido.
                                    heapq.heappush(open_set, (f_score[neighbor], tentative_g_score, neighbor))
            return []

        # Corrige uma cagada que eu fiz, estava considerando como objeto o PILL, mas é coordenada
        if pills:
            pill_coords = [(pill.x, pill.y) for pill in pills]
            nearest_pill = min(pill_coords, key=lambda p: heuristic((self.x, self.y), p))

            # Monta o caminho de A*
            path = a_star((self.x, self.y), nearest_pill)
            if path:
                next_step = path[0]
                self.x, self.y = next_step

                # Atualiza a posição
                self.update_position()

        # -------------------------------------
        # NÃO MEXER!!!!!!!
        self.eat_pills(pills) # Não apague!
        # -------------------------------------

        # return True

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)