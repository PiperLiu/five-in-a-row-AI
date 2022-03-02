from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS

from config import CONFIG
from game import Board
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet
from utils import get_model_path

app = Flask(__name__)
api = Api(app)
CORS(app, supports_credentials=True)

policy = PolicyValueNet(CONFIG['BOARD_WIDTH'], CONFIG['BOARD_HEIGHT'],
                        get_model_path(CONFIG['MODEL_NAME']))

MCTSPlayer = MCTSPlayer(policy.policy_value_fn,
                        c_puct=CONFIG['C_PUCT'], n_playout=CONFIG['N_PLAYOUT'])

class AiChess(Resource):
    def get_ai_move(self, states, player, last_move):
        board = Board()
        board.force_to_state(states, player, last_move)
        move = MCTSPlayer.get_action(board)
        return move

    def post(self):
        data = request.get_json(force=True)
        player = int(data['player'])
        states = {}
        for key in data['states']:
            states[int(key)] = int(data['states'][key])
        last_move = int(data['last_move'])
        assert player in (1, 2), f'player is {player}'
        assert states[last_move] != player, f'上次移动 {last_move} 还是 {player} 做的'
        move = self.get_ai_move(states, player, last_move)
        return float(move)

api.add_resource(AiChess, '/aichess')

if __name__ == '__main__':
    app.run(debug=CONFIG['debug'])
