import pygame
import sys
from ghosts.ghost import *
from game.pill import Pill
from game.config import *
from players.setup import *
from ghosts.setup import *

# Adicione o seu agente aqui!
agents = [
    CINDY_LAUPER,
    DAVID_BOWIE,
    FREDDIE_MERCURY,
    GEORGE_MICHAEL,
    MADONNA,
    # NOME_DO_SEU_AGENTE
]

AGENT_SCORES = {agent.name: agent.score for agent in agents}

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

def draw_text(screen, agents):
    font_path = 'src/game/PressStart2P-Regular.ttf'
    font = pygame.font.Font(font_path, 23)
    
    text_surface = font.render("RINHA DE PAC-MAN", True, WHITE)   
    text_x = WIDTH - 390
    text_y = 30
    screen.blit(text_surface, (text_x, text_y))
    
    score_font = pygame.font.Font(font_path, 18)
    score_y = text_y + 40 

    for agent in agents:
        if agent.name in AGENT_SCORES:
            if agent.alive:
                status_color = BLACK
            else:
                status_color = RED

            x_surface = score_font.render("X ", True, status_color)
            name_surface = score_font.render(agent.name, True, agent.color)
            score_surface = score_font.render(f": {AGENT_SCORES[agent.name]}", True, agent.color)

            screen.blit(x_surface, (text_x, score_y))
            screen.blit(name_surface, (text_x + x_surface.get_width(), score_y))
            screen.blit(score_surface, (text_x + x_surface.get_width() + name_surface.get_width(), score_y))
            
            score_y += 30

# Inicialização dos fantasmas e agentes
ghosts = [
    BLINKY,
    CLYDE,
    INKY, 
    PINKY
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
    
    # segue o baile pra quem não foi de arrasta
    for agent in agents:
        if agent.alive:
            agent.move(pills)
            agent.update_position()
            AGENT_SCORES[agent.name] = agent.score
    
    # faz os fantasmas perseguirem os agentes que estão vivos
    for ghost in ghosts:
        for agent in agents:
            if agent.alive:
                ghost.move(agent)
    
    # verifica colisões
    for ghost in ghosts:
        for agent in agents:
            if ghost.check_collision(agent) and agent.alive:
                agent.alive = False
                AGENT_SCORES[agent.name] = agent.score

    screen.fill(BLACK)
    draw_maze(screen, pills)
    draw_text(screen, agents)
    
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
