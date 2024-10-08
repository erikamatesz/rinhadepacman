import os

# obtém o caminho absoluto para a fonte pra não dar problema no Windows
base_dir = os.path.dirname(__file__)
FONT_PATH = os.path.join(base_dir, 'PressStart2P-Regular.ttf')

# tela
WIDTH, HEIGHT = 1400, 740
FPS = 15
TILE_SIZE = 24

# cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)    
PINK = (255, 182, 193)  
CYAN = (0, 255, 255)    
ORANGE = (255, 165, 0)

# labirinto
MAZE = [
    "#########################################",
    "#.......................................#",
    "#.###.####.##.####.####.####.####.#####.#",
    "#.###.####.##.####.####.####.####.#####.#",
    "#.###.####.##.####.####.####.####.#####.#",
    "#.................................#####.#",
    "#.####.##.####.###########.####.#.......#",
    "#.####.##.####.###########.####.####.##.#",
    "#.####.##.####.###########.####.####.##.#",
    "#...........##.###########.##...........#",
    "#.####.####.##.............##.####.####.#",
    "#.####.####.##.####.####.####.####.####.#",
    "#.####.####.##.####.####.####.####.####.#",
    "#.####..................................#",
    "#.####.######.#######.#########.##.####.#",
    "#.......................................#",
    "#.###.###.##.##.##.####.####.##.##.####.#",
    "#.###.###.##.##.##.####.####....##.####.#",
    "#.###.###.##.##.##.####.##...##.##.####.#",
    "#.###.###.##.##.##.####.##.####.##.####.#",
    "#.###.###.##.##.##.####.##.####.##.####.#",
    "#.......................................#",
    "#.####.######.#############.#######.###.#",
    "#.####........#############.#######.###.#",
    "#.####.######.######........#######.###.#",
    "#......######.######.######.#######.###.#",
    "#.####........######.######.#######.....#",
    "#.####.######........######.........###.#",
    "#.####.#########.###.##################.#",
    "#.......................................#",
    "#########################################"
]

# variável global que vai armazenar as posições de todos os agentes no jogo
AGENTS_POSITIONS = {}

# variável global que vai armazenar os scores dos agentes
AGENT_SCORES = {}
