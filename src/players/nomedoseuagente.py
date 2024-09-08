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

#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class NomeDoSeuAgente(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial 
        # do seu Pac-Man na planilha.
        x = 0
        y = 0
        color = (0, 0, 0) # Coloque aqui o código RGB do seu Pac-Man.
        super().__init__("Nome do seu Pac-Man", x, y, color) # Atualize o nome dele.
        self.update_position()
    
    def move(self, pills):
        # Lembre-se que você tem acesso às variáveis MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------


        # ------------------------------ Final da sua implementação -----------------------------------------

        self.eat_pills(pills) # Não apague!

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)
        
