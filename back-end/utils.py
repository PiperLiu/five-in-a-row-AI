import os.path as osp
import time
from config import *

PWD = osp.dirname(__file__)
MODEL_DIR = osp.join(PWD, 'models')
TRAIN_DATA_DIR = osp.join(PWD, 'logs')

def get_model_path(filename):
    return osp.join(MODEL_DIR, filename)

