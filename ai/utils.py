import os.path as osp
import time
from config import *

PWD = osp.dirname(__file__)
MODEL_DIR = osp.join(PWD, 'models')
TRAIN_DATA_DIR = osp.join(PWD, 'logs')

def get_model_path(filename):
    return osp.join(MODEL_DIR, filename)

def get_log_path(filename):
    return osp.join(TRAIN_DATA_DIR, filename)

def get_default_name():
    res = f"{time.strftime('%Y%m%d%H%M', time.localtime())}" + \
          f"_{BOARD_WIDTH}_{BOARD_HEIGHT}_{N_IN_ROW}" + \
          f"_{TEMP}_{C_PUCT}_{N_PLAYOUT}"
    return res
