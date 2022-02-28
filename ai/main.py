from train import TrainPipeline
from utils import get_model_path, get_default_name
from config import globalV
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-m', '--model', type=str, default=None)

if __name__ == "__main__":
    args = parser.parse_args()

    if args.model is not None:
        globalV['MODEL_NAME'] = args.model
        globalV['MODEL_PATH'] = get_model_path(args.model)
    else:
        globalV['MODEL_NAME'] = get_default_name()
        globalV['MODEL_PATH'] = None

    training_pipeline = TrainPipeline(globalV['MODEL_PATH'])
    training_pipeline.run()
