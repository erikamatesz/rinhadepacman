import pygame
import os
from ghosts.ghost import *
from game.pill import Pill
from game.config import *
from players.setup import *
from ghosts.setup import *

# obtém o caminho absoluto para a fonte pra não dar problema no Windows
base_dir = os.path.dirname(__file__)
font_path = os.path.join(base_dir, 'game', 'PressStart2P-Regular.ttf')

# adicione o seu agente aqui!
agents = [
    # CINDY_LAUPER,
    # DAVID_BOWIE,
    # FREDDIE_MERCURY,
    # GEORGE_MICHAEL,
    # MADONNA,
    BANGUELA,
    BILBO,
    JUVENAL,
    KAWABANGA,
    LABIRINTHIS,
    LUPS,
    NEO,
    NIELSEN,
    PIKACHU,
    RAPADURA,
    SEMNOME,
    STITCH,
    TAZ,
    YODA
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

def draw_text(screen, agents, game_over, winner=None):
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
    
    if game_over:
        end_game_font = pygame.font.Font(font_path, 18)
        end_game_surface = end_game_font.render("Fim de jogo!", True, WHITE)
        screen.blit(end_game_surface, (text_x, score_y + 30))
        
        if winner:
            winner_surface = end_game_font.render(f"{winner.name} ganhou!", True, WHITE)
            screen.blit(winner_surface, (text_x, score_y + 60))

def calculate_max_possible_score(agent, pills):
    return agent.score + len(pills)

def check_if_last_agent_can_win(agents, pills):
    alive_agents = [agent for agent in agents if agent.alive]
    if len(alive_agents) == 1:
        last_agent = alive_agents[0]
        max_possible_score = calculate_max_possible_score(last_agent, pills)
        dead_agents_scores = [AGENT_SCORES[agent.name] for agent in agents if not agent.alive]
        
        if dead_agents_scores and max_possible_score <= max(dead_agents_scores):
            return False
    return True

def find_winner(agents):
    return max(agents, key=lambda agent: AGENT_SCORES[agent.name])

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
game_over = False
winner = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_over:
        pass
    else:
        # verifica se todas as pílulas foram comidas
        if not any(pill.eaten is False for pill in pills):
            game_over = True
            winner = find_winner(agents)

        # verifica se todos os agentes foram comidos
        elif all(not agent.alive for agent in agents):
            game_over = True
            winner = find_winner(agents)

        # seeee não foram... verifica se há apenas um agente e se ele não pode mais vencer
        elif len([agent for agent in agents if agent.alive]) == 1:
            if not check_if_last_agent_can_win(agents, pills):
                game_over = True
                winner = find_winner(agents)
    
        # segue o baile pra quem não foi de arrasta
        for agent in agents:
            if agent.alive:
                agent.move(pills)
                agent.update_position()
                AGENT_SCORES[agent.name] = agent.score
    
        for ghost in ghosts:
            for agent in agents:
                if agent.alive:
                    ghost.move(agent)
    
        # colisões
        for ghost in ghosts:
            for agent in agents:
                if ghost.check_collision(agent) and agent.alive:
                    agent.alive = False
                    AGENT_SCORES[agent.name] = agent.score

    screen.fill(BLACK)
    draw_maze(screen, pills)
    draw_text(screen, agents, game_over, winner)
    
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
