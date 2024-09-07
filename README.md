# Rinha de Pac-Man

Por favor, leia tudo! 💛

## Regras do jogo

1. O tabuleiro tem um tamanho fixo no qual os espaços em azul são paredes e os espaços em preto são caminhos que formam um labirinto.
2. Quatro fantasmas (quadradinhos) serão posicionados um em cada canto do tabuleiro e sua movimentação é aleatória. 
3. O jogo terá mais de um Pac-Man (bolinha), cada um deles será um agente.
4. Quando um fantasma encosta em algum Pac-Man, ele morre e é removido do tabuleiro.
5. Contrariando o que acontece muitas vezes no transporte público do Rio de Janeiro: dois corpos não ocupam o mesmo lugar que um.
6. Os caminhos do labirinto são formados por pílulas (bolinhas brancas) que podem ser comidas por qualquer Pac-Man.
7. Cada bolinha branca comida vale 1 ponto.

## Setup do projeto

Estas instruções funcionarão no macOS e em distribuições do Linux.

Para prosseguir, você precisa ter o Python 3.9 ou superior instalado.

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

Recomendo a utilização do Visual Studio Code para testar o projeto em sua máquina e desenvolver o seu agente.

## Codando o seu agente