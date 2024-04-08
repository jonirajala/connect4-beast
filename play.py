import numpy as np
from game import Game
from mcts import mcts, simple_mcts


def random_player(game, board):
    allowed_moves = game.allowed_moves(board)
    return np.random.choice(allowed_moves)

game = Game()
board, player = game.init_env()
state = "Continue"
while state == "Continue":
    game.draw(board)
    if player == 1:
        # move = int(input(f"Player {player} move: "))
        # while not game.is_allowed(move, board):
        #     print("Invalid Move")
        #     move = int(input(f"Player {player} move: "))

        move = simple_mcts(game, board, player, 400)
    else:
        move = mcts(game, board, player, 400)

    state, board = game.play_move(move, board, player)
    player *= -1

game.draw(board)
players = {1:"simple", -1:"complex"}
if state == "Win":
    print(f"Player {players[-player]} wins")
else:
    print(state)
