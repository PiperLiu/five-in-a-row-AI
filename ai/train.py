import random
import numpy as np
from collections import deque
from torch.utils.tensorboard import SummaryWriter

from utils import get_log_path, get_model_path
from game import Board, Game
from mcts_alphaZero import MCTSPlayer
from policy_value_net_pytorch import PolicyValueNet
from config import BOARD_HEIGHT, BOARD_WIDTH, N_IN_ROW, \
        TEMP, C_PUCT, N_PLAYOUT, LEARNING_RATE, BUTTER_SIZE, BATCH_SIZE, \
        CHECK_FREQ, GAME_BATCH_NUM, globalV

class TrainPipeline:
    def __init__(self, init_model=None):
        # 棋盘相关参数
        self.board_width = BOARD_WIDTH
        self.board_height = BOARD_HEIGHT
        self.n_in_row = N_IN_ROW
        self.board = Board(
            width=self.board_width,
            height=self.board_height,
            n_in_row=self.n_in_row
        )
        self.game = Game(self.board)
        # 自我对弈相关参数
        self.temp = TEMP
        self.c_puct = C_PUCT
        self.n_playout = N_PLAYOUT
        # 训练更新相关参数
        self.learn_rate = LEARNING_RATE
        self.buffer_size = BUTTER_SIZE
        self.batch_size = BATCH_SIZE
        self.data_buffer = deque(maxlen=self.buffer_size)
        self.check_freq = CHECK_FREQ  # 保存模型的概率
        self.game_batch_num = GAME_BATCH_NUM # 训练更新的次数
        if init_model:
            # 如果提供了初始模型，则加载其用于初始化策略价值网络
            self.policy_value_net = PolicyValueNet(
                self.board_width,
                self.board_height,
                model_file=init_model
            )
        else:
            # 随机初始化策略价值网络
            self.policy_value_net = PolicyValueNet(
                self.board_width,
                self.board_height
            )
            globalV['MODEL_PATH'] = get_model_path(globalV['MODEL_NAME'])
        self.mcts_player = MCTSPlayer(
            self.policy_value_net.policy_value_fn,
            c_puct=self.c_puct,
            n_playout=self.n_playout,
            is_selfplay=1
        )
        self.tb = SummaryWriter(get_log_path(globalV['MODEL_NAME']))

    def run(self):
        """ 执行完整的训练流程 """
        for i in range(self.game_batch_num):
            episode_len = self.collect_selfplay_data()
            if len(self.data_buffer) > self.batch_size:
                loss, entropy = self.policy_update()
                print((
                    "batch i:{}, "
                    "episode_len:{}, "
                    "loss:{:.4f}, "
                    "entropy:{:.4f}"
                ).format(i+1, episode_len, loss, entropy))
                # save performance per update
                self.tb.add_scalar('episode_len', episode_len, i+1)
                self.tb.add_scalar('loss', loss, i+1)
                self.tb.add_scalar('entropy', entropy, i+1)
            else:
                print("batch i:{}, episode_len:{}".format(i+1, episode_len))
            # 定期保存模型
            if (i+1) % self.check_freq == 0:
                self.policy_value_net.save_model(globalV['MODEL_PATH'])

    def collect_selfplay_data(self):
        """ collect self-play data for training """
        winner, play_data = self.game.start_self_play(self.mcts_player, temp=self.temp)
        play_data = list(play_data)[:]
        episode_len = len(play_data)
        # augment the data
        play_data = self.get_equi_data(play_data)
        self.data_buffer.extend(play_data)
        return episode_len

    def get_equi_data(self, play_data):
        """ play_data: [(state, mcts_prob, winner_z), ...] """
        extend_data = []
        for state, mcts_prob, winner in play_data:
            for i in [1, 2, 3, 4]:
                # 逆时针旋转
                equi_state = np.array([np.rot90(s, i) for s in state])
                equi_mcts_prob = np.rot90(np.flipud(
                    mcts_prob.reshape(self.board_height, self.board_width)
                ), i)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))
                # 水平翻转
                equi_state = np.array([np.fliplr(s) for s in equi_state])
                equi_mcts_prob = np.fliplr(equi_mcts_prob)
                extend_data.append((equi_state, np.flipud(equi_mcts_prob).flatten(), winner))
        return extend_data

    def policy_update(self):
        """ update the policy-value net """
        mini_batch = random.sample(self.data_buffer, self.batch_size)
        state_batch = [data[0] for data in mini_batch]
        mcts_probs_batch = [data[1] for data in mini_batch]
        winner_batch = [data[2] for data in mini_batch]
        loss, entropy = self.policy_value_net.train_step(
            state_batch, mcts_probs_batch, winner_batch, self.learn_rate
        )
        return loss, entropy
