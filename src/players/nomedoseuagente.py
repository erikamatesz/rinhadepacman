# escolha um nome para o seu agente e renomeie o arquivo e a classe.
# não altere os imports que já existem nela. se precisar adicionar imports, 

from players.pacman import Pacman
from game.config import *

class NomeDoSeuAgente(Pacman):
    def __init__(self):
        x = 0 # defina aqui o x inicial
        y = 0 # defina aqui o y inicial
        color = (0, 0, 0) # defina uma cor usando o RGB - https://www.w3schools.com/colors/colors_picker.asp
        super().__init__("Nome do seu agent", x, y, color)
    
    def move(self, maze, pills):
        # ------------------------------ início da sua implementação ----------------------------------------


        # ------------------------------ final da sua implementação -----------------------------------------
        self.eat_pills(pills) # não apague!
