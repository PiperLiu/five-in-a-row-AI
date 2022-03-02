from typing import Dict


CONFIG: Dict = {
    'debug': False,

    # 棋盘配置
    'BOARD_WIDTH': 8,
    'BOARD_HEIGHT': 8,
    'N_IN_ROW': 5,

    # 权重名称
    'MODEL_NAME': 'current_policy_1.model',

    # MCTS
    'TEMP': 1.0,
    'C_PUCT': 5,
    'N_PLAYOUT': 400,
}
