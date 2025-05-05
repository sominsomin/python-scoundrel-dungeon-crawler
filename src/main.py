from entities.Game import Game
from blessed import Terminal

game_run = True

if __name__ == "__main__":
    game = Game()

    while game_run is True:
        game.run()
        game_run = False
