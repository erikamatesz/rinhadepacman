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
from queue import PriorityQueue


#
# Renomeie a classe para o nome do seu Pac-Man. Se ele se chama Alfredinho Maravilha, 
# então a classe será AlfredinhoMaravilha e o arquivo será alfredinhomaravilha.py, ok?
# Não esqueça de atualizar as informações onde está sinalizado!
#

class Banguela(Pacman):
    def __init__(self):
        # Troque os valores de X e Y para os que você escolheu como posição inicial 
        # do seu Pac-Man na planilha.
        x = 18
        y = 18
        color = (107, 63, 160) # Coloque aqui o código RGB do seu Pac-Man.

        # ------------------------------ Minhas inicializações ----------------------------------------------
        self.grid = []
        self.mapa = {} # Dictionary para armazenar as coordenadas e seus caminhos possíveis
        self.caminho_final = []  # Armazenará o caminho como uma lista de passos
        self.step_index = 0  # Index para seguir o caminho passo a passo

        self.rows = len(MAZE) - 2
        self.cols = len(MAZE) - 2

        self.destino = None  # O target atual

        self.rotas_fuga = [(21, 14), (1, 5), (10, 15), (18, 18)]

        for y_ in range(1, len(MAZE) - 1):  # Ignorar primeira e última linha
            for x_ in range(1, len(MAZE[y_]) - 1):  # Ignorar primeira e última coluna
                self.grid.append((x_, y_))

        # Iterar sobre o array MAZE, desprezando as extremidades
        for x__ in range(1, len(MAZE[0]) - 1):  # Iterar sobre as colunas (ignorar primeira e última)
            for y__ in range(1, len(MAZE) - 1):  # Iterar sobre as linhas (ignorar primeira e última)
                if MAZE[y__][x__] == '.':  # Verifica se a célula é um caminho ('.')
                    # Verificar caminhos em cada direção (Norte, Sul, Leste, Oeste)
                    self.mapa[(x__, y__)] = {
                        'N': 1 if MAZE[y__-1][x__] == '.' else 0,  # Norte (acima)
                        'S': 1 if MAZE[y__+1][x__] == '.' else 0,  # Sul (abaixo)
                        'L': 1 if MAZE[y__][x__+1] == '.' else 0,  # Leste (direita)
                        'O': 1 if MAZE[y__][x__-1] == '.' else 0   # Oeste (esquerda)
                    }
        # ---------------------------------------------------------------------------------------------------
   

        super().__init__("Banguela", x, y, color) # Atualize o nome dele.
        self.update_position()
    
    def move(self, pills):
        # Lembre-se que, além da variável pills, você tem acesso às variáveis globais MAZE e AGENTS_POSITIONS!

        # ------------------------------ Início da sua implementação ----------------------------------------
        # Detectar agentes próximos
        agentes_proximos = self.detectar_agentes_proximos()

        # Se houver agentes próximos e o Pac-Man não estiver em fuga, escolher a rota de fuga
        if agentes_proximos and not getattr(self, 'em_fuga', False):
            rota_fuga = self.escolher_rota_fuga()
            self.destino = rota_fuga
            self.caminho_final = self.aestrela()  # Calcular o caminho para a rota de fuga
            self.step_index = 0
            self.em_fuga = True  # Marcar que o Pac-Man está em fuga

        # Se o Pac-Man está em fuga, seguir para a rota de fuga
        if getattr(self, 'em_fuga', False):
            if self.caminho_final and self.step_index < len(self.caminho_final):
                proxima_celula = self.caminho_final[self.step_index][1]
                self.x, self.y = proxima_celula
                self.step_index += 1

                # Se o Pac-Man atingir a rota de fuga, sair do estado de fuga e buscar a pill mais próxima
                if (self.x, self.y) == self.destino:
                    self.caminho_final = []
                    self.step_index = 0
                    self.em_fuga = False  # Sair do modo de fuga
                    pill_proxima = self.pill_mais_proxima(pills)  # Buscar a pill mais próxima
                    if pill_proxima:
                        self.destino = (pill_proxima.x, pill_proxima.y)
                        self.caminho_final = self.aestrela()  # Calcular o caminho para a pill
                        self.step_index = 0

        # Se não há fuga, seguir o movimento normal para a pill mais próxima
        if not getattr(self, 'em_fuga', False):
            pill_proxima = self.pill_mais_proxima(pills)

            if pill_proxima:
                self.destino = (pill_proxima.x, pill_proxima.y)

                if not self.caminho_final or (self.x, self.y) == self.destino:
                    self.caminho_final = self.aestrela()
                    self.step_index = 0

            # Movimentar o Pac-Man ao longo do caminho calculado para a pill
            if self.caminho_final and self.step_index < len(self.caminho_final):
                proxima_celula = self.caminho_final[self.step_index][1]
                self.x, self.y = proxima_celula
                self.step_index += 1

            if (self.x, self.y) == self.destino:
                self.caminho_final = []
                self.step_index = 0

    
        # ------------------------------ Final da sua implementação -----------------------------------------

        self.eat_pills(pills) # Não apague!

    # Aqui é onde o seu Pac-Man vai atualizar a variável global AGENTS_POSITIONS com a posição atual dele.
    # Não altere essa implementação!
    def update_position(self):
        AGENTS_POSITIONS[self.name] = (self.x, self.y)

    # ---------------------------------- Meus métodos ------------------------------------------------------- 
    def h_score(self, celula, destino):
        colunac = celula[0]  # Primeiro valor é a coluna
        linhac = celula[1]   # Segundo valor é a linha
        colunad = destino[0]  # Primeiro valor é a coluna do destino
        linhad = destino[1]   # Segundo valor é a linha do destino
        return abs(colunac - colunad) + abs(linhac - linhad)    

    def aestrela(self):

        #criar tabuleiro com todos com f_score infinito
        f_score = {celula: float("inf") for celula in self.grid}
        g_score = {}

        celula_inicial = (self.x, self.y)

        g_score[celula_inicial] = 0
        f_score[celula_inicial] = g_score[celula_inicial] + self.h_score(celula_inicial, self.destino)

        fila = PriorityQueue()
        item = (f_score[celula_inicial], self.h_score(celula_inicial, self.destino), celula_inicial)
        fila.put(item)

        caminho = {}

        while not fila.empty():
            celula = fila.get()[2]

            if(celula == self.destino):
                break

            for direcao in "NSLO":
                if self.mapa[celula][direcao] == 1:
                    coluna_celula = celula[0]  # Agora o primeiro valor é a coluna
                    linha_celula = celula[1]   # O segundo valor é a linha

                    if direcao == "N":
                        proxima_celula = (coluna_celula, linha_celula - 1)  # Norte: move para cima (diminuir linha)
                    elif direcao == "S":
                        proxima_celula = (coluna_celula, linha_celula + 1)  # Sul: move para baixo (aumentar linha)
                    elif direcao == "L":
                        proxima_celula = (coluna_celula + 1, linha_celula)  # Leste: move para a direita (aumentar coluna)
                    elif direcao == "O":
                        proxima_celula = (coluna_celula - 1, linha_celula)  # Oeste: move para a esquerda (diminuir coluna)

                    novo_g_score = g_score[celula] + 1
                    novo_f_score = novo_g_score + self.h_score(proxima_celula, self.destino)

                    if novo_f_score < f_score[proxima_celula]:
                        f_score[proxima_celula] = novo_f_score
                        g_score[proxima_celula] = novo_g_score
                        item = (novo_f_score, self.h_score(proxima_celula, self.destino), proxima_celula)
                        fila.put(item)
                        caminho[proxima_celula] = celula

        caminho_final = {}
        celula_analisada = self.destino
        while celula_analisada != celula_inicial:
            caminho_final[caminho[celula_analisada]] = celula_analisada
            celula_analisada = caminho[celula_analisada]

        caminho_lista = list(caminho_final.items())
        caminho_lista.reverse()         

        return caminho_lista

    def pill_mais_proxima(self, pills):
        posicao_atual = (self.x, self.y)
        menor_distancia = float('inf')
        pill_proxima = None

        for pill in pills:
            if not pill.eaten:  # Verifica se a pill ainda não foi comida
                distancia = self.h_score(posicao_atual, (pill.x, pill.y))
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    pill_proxima = pill

        return pill_proxima

    def detectar_agentes_proximos(self, raio_fuga=2):
        # Verificar se há fantasmas ou Pac-Mans a uma distância menor ou igual a 'raio_fuga'
        posicao_atual = (self.x, self.y)
        agentes_proximos = []

        # Percorrer todas as posições dos agentes no jogo
        for agente, posicao in AGENTS_POSITIONS.items():
            if agente != self.name:  # Ignorar a própria posição do Pac-Man
                distancia = self.h_score(posicao_atual, posicao)  # Calcular a distância de Manhattan
                if distancia <= raio_fuga:  # Se estiver dentro do raio de duas casas
                    agentes_proximos.append((agente, posicao))

        return agentes_proximos

    def escolher_rota_fuga(self):
        posicao_atual = (self.x, self.y)
        rota_fuga_mais_distante = None
        maior_distancia = -1

        # Verificar a distância de Manhattan para cada rota de fuga
        for rota in self.rotas_fuga:
            distancia = self.h_score(posicao_atual, rota)
            if distancia > maior_distancia:
                maior_distancia = distancia
                rota_fuga_mais_distante = rota

        return rota_fuga_mais_distante
