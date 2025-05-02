from entities.Game import Game
from blessed import Terminal

game_run = True

if __name__=='__main__':
    game = Game()


    while game_run is True:
        game.run()

        # print(term.home + term.clear + term.move_y(term.height // 2))
        # print(term.black_on_darkkhaki(term.center('press any key to continue.')))

        # with term.cbreak(), term.hidden_cursor():
        #     inp = term.inkey()

        # print(term.move_down(2) + 'You pressed ' + term.bold(repr(inp)))

        game_run = False