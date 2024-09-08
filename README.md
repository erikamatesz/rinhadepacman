# Rinha de Pac-Man

Tentei colocar o máximo de informações para ajudar todo mundo, portanto, por favor, leia tudo com atenção! 💛

Este `README` possui as seguintes seções:

- Conhecendo o Jogo
    - Objetivos do seu Pac-Man
    - Tabuleiro e Pílulas
    - Variável `AGENTS_POSITIONS`
    - Fantasmas

- Setup do Projeto
    - macOS e Linux
    - Windows

- Rodando o Jogo SEM o seu Pac-Man

- Codando seu Pac-Man
    - Como Testar o seu Pac-Man
    - Como Enviar

## Conhecendo o Jogo

### Objetivos do seu Pac-Man

1 - Não ser pego pelos fantasmas.
2 - Comer o maior número de pílulas.

### Tabuleiro e Pílulas

O tabuleiro é representado por uma variável estática `MAZE`, ou seja, que não se altera ao longo do jogo. Essa variável é uma lista de strings.

Em cada string, os espaços representados por # correspondem às paredes e vão aparecer na cor azul. Já os espaços representados por . correspondem aos caminhos e vão aparecer na cor preta.

Os personagens - seja um fantasma, seja um Pac-Man - só se movimentam pelos caminhos do labirinto.

Quando o jogo é iniciado, todos os caminhos estarão preenchidos por pílulas brancas que são representadas por bolinhas brancas. Quando a pílula é comida, a bolinha branca que a representa deixa de existir ficando apenas o espaço preto.

Nesta implementação, não haverá a lógica da "super pílula" que permite que o Pac-Man mate os fantasmas. Também não haverá a "frutinha".

Cada pílula comida vale 1 ponto para o Pac-Man que a comeu.

A classe que define a pílula é `src/game/pill.py` e uma lista com as pílulas é passada para o Pac-Man.

```py
# Variável MAZE

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

# Exemplo de como acessar o elemento na linha 1, coluna 1

linha = 1
coluna = 1
celula = MAZE[linha][coluna]
print(celula)  # Saída: '.'
```

### Variável `AGENTS_POSITIONS`

A cada movimentação, seja ela de um fantasma ou de um Pac-Man, a posição do personagem será registrada na variável `AGENTS_POSITIONS` que é global. Portanto, através dessa variável, você tem como saber onde estão todos os fantasmas e também cada Pac-Man que ainda esteja vivo no jogo.

**IMPORTANTE!**

Um personagem Pac-Man e um personagem fantasma não podem ocupar o mesmo espaço porque isso significa que o fantasma pegou o Pac-Man, sua estratégia deverá evitar que isso aconteça, pois quanto mais tempo o seu Pac-Man permanecer no tabuleiro, mais chances ele tem que encontrar e comer pílulas.

Dois personagens do tipo Pac-Man não podem ocupar o mesmo espaço, portanto, você terá que elaborar a sua estratégia para evitar isso.

```py
# Exemplo da variável se tivermos um Pac-Man chamado Cindy Lauper e um Pac-Man chamado David Bowie

AGENTS_POSITIONS = {
    "Cindy Lauper": (5, 10),
    "David Bowie": (7, 12),
    "Clyde": (3, 8),
    "Blinky": (5, 9),  
    "Inky": (2, 8),
    "Pinky": (1, 1)
}

print(AGENTS_POSITIONS["Inky"])  # Saída: (2, 8)

# Pegando todas as posições ocupadas
posicoes_ocupadas = list(AGENTS_POSITIONS.values())

# Exibindo as posições ocupadas
print(posicoes_ocupadas)

# Saída: [(5, 10), (7, 12), (3, 8), (5, 9), (2, 8), (1, 1)]
```

Quando um Pac-Man é pego por um fantasma, ele deixa de aparecer em `AGENTS_POSITIONS`.

### Fantasmas

Serão quatro fantasmas que se movimentarão de maneira aleatória no tabuleiro. As posições iniciais deles são as seguintes:

- Blinky (vermelho): coluna 1, linha 1 -> Canto superior esquerdo.
- Inky (ciano): coluna 39, linha 1 -> Canto superior direito.
- Pinky (rosa): coluna 1, linha 29 -> Canto inferior esquerdo.
- Clyde (laranja): coluna 39, linha 29 -> Canto inferior direito.

As posições que os fantasmas ocupam são registradas na variável global `AGENTS_POSITIONS` conforme mostrado na seção anterior.

Quando um fantasma ocupa a mesma posição de um Pac-Man, ele "mata" aquele Pac-Man.

## Setup do projeto 

Para prosseguir, você precisa ter o Python 3.9 ou superior instalado na sua máquina.

Recomendo a utilização do Visual Studio Code para testar o projeto em sua máquina e desenvolver o seu Pac-Man.

### macOS e Linux

Crie um ambiente virtual. Eu escolhi o nome `rinha` que é o que consta no arquivo `.gitignore`, mas você pode escolher o que quiser.

```sh
python3 -m venv rinha
```

Em seguida, ative o ambiente virtual.

```sh
source rinha/bin/activate
```

Ao fazer isso, você verá o nome do ambiente no prompt do terminal entre parênteses, indicando que ele está ativo.

Instale as dependências do projeto.

```sh
pip install -r requirements.txt
```

Quando quiser desativar o ambiente virtual, utilize o comando `deactivate` no terminal.

# Windows

Como eu não tenho máquina Windows, não tenho como verificar se essas etapas vão funcionar direitinho :(

Você precisa ter o Python instalado corretamente e adicionado ao PATH para poder executar os comandos abaixo.

Abra o terminal ou o Prompt de Comando (cmd) ou o PowerShell e navegue até o diretório onde você baixou ou clonou o projeto e execute o comando a seguir:

```sh
# pode ser que seja python3 o comando
python -m venv rinha
```

Para ativar o ambiente virtual, use o seguinte comando:

```sh
# se estiver usando o cmd:
rinha\Scripts\activate

# ou se estiver usando o PowerShell:
.\rinha\Scripts\Activate
```

Instale as dependências do projeto.

```sh
pip install -r requirements.txt
```

Quando quiser desativar o ambiente virtual, utilize o comando `deactivate` no cmd ou no PowerShell.

## Rodando o Jogo SEM o seu Pac-Man

Se o setup foi bem sucedido, você tem duas maneiras de rodar o jogo.

Caso você esteja usando o Visual Studio Code, ao abrir o arquivo `run.py` localizado na raiz do projeto, você pode clicar no botão com o símbolo de "play" que fica no canto superior direito da janela onde o código aparece.

Caso você esteja utilizando outra IDE ou o botão que eu mencionei não esteja aparecendo, não tem problema. Vá até o diretório onde está o projeto e rode o comando abaixo:

```sh
python3 src/run.py
```

Se tudo estiver funcionando direitinho, o jogo aparece em uma janela.

Deixei alguns agentes preparados no jogo para que você possa ver como funciona. Eles não se movimentam com nenhum algoritmo em especial, estão se movimentando aleatoriamente, assim como os fantasmas.

## Codando o seu Pac-Man

**IMPORTANTE:** Antes de mais nada, [visite esta planilha aqui](https://docs.google.com/spreadsheets/d/1KwM8qYp8d0s_5_A6uOOHChuq5coZgEol/edit?usp=sharing&ouid=109929369500005214820&rtpof=true&sd=true)!

Nela você vai poder visualizar o mapa, escolher uma posição inicial para o seu Pac-Man, colocar o nome dele no quadro e a cor que você escolheu para representá-lo.

É importante preencher esses dados para que não tenhamos um Pac-Man começando na mesma posição do outro e agentes com as mesmas cores ou de outro Pac-Man ou dos fantasmas.

Feito isso, bora codar! :)

Toda a estrutura do jogo está pronta e você não precisa alterar nada que não seja o seu próprio Pac-Man, ok?

Na pasta `src/players` você encontra os arquivos referentes aos agentes disponíveis, além de alguns outros.

Abra o arquivo `nomedoseuagente.py` e leia atentamente as instruções contidas nele.

**Você vai implementar o seu código ali e somente ali.**

### Como Testar o seu Pac-Man

Depois de codar o seu agente e já ter renomeado / alterado tudo o que é solicitado, abra o arquivo `src/players/setup.py` e siga as instruções dele.

Basicamente, em `setup.py` você vai importar e instanciar o seu Pac-Man.

A instrução final contida em `setup.py` pede que você abra o arquivo `run.py` e altere esta parte:

```py
# Adicione o seu agente aqui!
agents = [
    CINDY_LAUPER,
    DAVID_BOWIE,
    FREDDIE_MERCURY,
    GEORGE_MICHAEL,
    MADONNA,
    # NOME_DO_SEU_AGENTE
]
```

### Como Enviar

Quando você terminar de codar e testar seu Pac-Man, envie somente o arquivo do seu agente para a pasta indicada [no drive](https://drive.google.com/drive/folders/1dfTdQ-G3b0Hp_PDBVmN0Arq2nGvcQ7oe?usp=drive_link).

Não deixe de sinalizar nos comentários do arquivo se precisou inserir alguma dependência no `requirements.txt`, ok?
