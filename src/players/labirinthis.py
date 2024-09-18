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
import pygame
from players.pacman import Pacman
from game.config import *
import random
#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#
class Labirinthis(Pacman):
    def __init__(self):
        x = 23
        y = 15
        color = (250, 200, 150)
        super().__init__("Labirinthis", x, y, color)
        self.update_position()
        # ------------------------------ Início da sua implementação ----------------------------------------
    def move(self, pills):
        # calculando a distância
        def manhattan_distance(x1, y1, x2, y2):
            return abs(x1 - x2) + abs(y1 - y2)

        # Encontrando as posições de pílulas restantes
        pill_positions = [(px, py) for px, row in enumerate(MAZE) for py, val in enumerate(row) if val == '.' and (py, px) in pills]

        # Fugindo dos inimigos
        enemy_positions = [pos for name, pos in AGENTS_POSITIONS.items() if name != self.name]

        # Verificando nova posição 
        def is_valid_move(nx, ny):
            return 0 <= ny < len(MAZE) and 0 <= nx < len(MAZE[0]) and MAZE[ny][nx] != '#' and (nx, ny) not in enemy_positions

        # Definindo os movimentos 
        possible_moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        #  buscando a pilula mais próxima 
        if pill_positions:
            target_pill = min(pill_positions, key=lambda p: manhattan_distance(self.x, self.y, p[1], p[0]))
            # Avaliação do movimento para a pílula mais próxima
            best_move = None
            min_distance = float('inf')

            for dx, dy in possible_moves:
                nx, ny = self.x + dx, self.y + dy
                if is_valid_move(nx, ny):
                    distance = manhattan_distance(nx, ny, target_pill[1], target_pill[0])
                    if distance < min_distance:
                        min_distance = distance
                        best_move = (dx, dy)
        else:
            # Acabando as pílulas, ande aleatório
            valid_moves = [(dx, dy) for dx, dy in possible_moves if is_valid_move(self.x + dx, self.y + dy)]
            best_move = random.choice(valid_moves) if valid_moves else None

        #  atualizando a posição
        if best_move:
            self.x += best_move[0]
            self.y += best_move[1]
            self.update_position()
        # ------------------------------ Final da sua implementação -----------------------------------------
        self.eat_pills(pills)  # Não apague!

    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
