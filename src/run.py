import pygame
from ghosts.ghost import *
from game.pill import Pill
from game.config import *
from players.setup import *
from ghosts.setup import *

def draw_maze(screen, pills):
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == '#':
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == '.':
                if not any(pill.x == x and pill.y == y and not pill.eaten for pill in pills):
                    pygame.draw.rect(screen, BLACK, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
                else:
                    pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 6)

ghosts = [
    BLINKY,
    CLYDE,
    INKY, 
    PINKY
]

# adicione o seu agente aqui
agents = [
    CINDY_LAUPER,
    DAVID_BOWIE,
    FREDDIE_MERCURY,
    GEORGE_MICHAEL,
    MADONNA,
    PRINCE,
    # NOME_DO_SEU_AGENTE
]

pills = []
for y, row in enumerate(MAZE):
    for x, tile in enumerate(row):
        if tile == '.':
            pills.append(Pill(x, y))

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rinha de Pac-Man")
clock = pygame.time.Clock()

# loop principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # quem não foi de arrasta...
    for agent in agents:
        if agent.alive:
            agent.move(MAZE, pills)
    
    # faz os fantasmas perseguirem os agentes
    for ghost in ghosts:
        for agent in agents:
            if agent.alive:
                ghost.move(agent, MAZE)
    
    # verifica colisões
    for ghost in ghosts:
        for agent in agents:
            if ghost.check_collision(agent) and agent.alive:
                print(f"{ghost.name} fez {agent.name} ir de arrasta!")
                agent.alive = False
    
    # score
    for agent in agents:
        agent.print_score()
    
    screen.fill(BLACK)
    draw_maze(screen, pills)
    
    for pill in pills:
        pill.draw(screen)
    
    for agent in agents:
        if agent.alive:
            agent.draw(screen)
    
    for ghost in ghosts:
        ghost.draw(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
