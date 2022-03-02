from glob import glob
from config import BOARD_HEIGHT, BOARD_WIDTH, N_IN_ROW
from utils import get_model_path
from config import globalV
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet

"""
input location as '3,3' to play
"""

class Human:
    """ human player """
    def __init__(self):
        self.player = None

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board):
        try:
            location = input("Your move: ")
            if isinstance(location, str):
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1
        if move == -1 or move not in board.available:
            print("invalid move")
            move = self.get_action(board)
        return move
    
    def __str__(self):
        return "Human {}".format(self.player)

def run(model_name):
    n = N_IN_ROW
    width, height = BOARD_WIDTH, BOARD_HEIGHT
    globalV['MODEL_NAME'] = model_name
    globalV['MODEL_PATH'] = get_model_path(model_name)
    try:
        board = Board(width=width, height=height, n_in_row=n)
        game = Game(board)
        # 创建 AI player
        best_policy = PolicyValueNet(width, height, model_file=globalV['MODEL_PATH'])
        mcts_player = MCTSPlayer(best_policy.policy_value_fn, c_puct=5, n_playout=400)
        # 创建 Human player ，输入样例： 2,3
        human = Human()
        # 设置 start_player = 0 可以让人类先手
        game.start_play(human, mcts_player, start_player=1, is_shown=1)
    except KeyboardInterrupt:
        print('\n\rquit')
