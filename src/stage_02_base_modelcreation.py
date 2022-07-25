import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml,create_directories
from src.utils.model import log_model_summary
import random
import tensorflow as tf


STAGE = "BASE MODEL CREATION" ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(params_path,config_path):
    ## read param files
    config = read_yaml(config_path)
    params = read_yaml(params_path)
    param = params['model_param']

    LAYERS = [
        tf.keras.layers.Input(shape=tuple(param['image_shape'])),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPool2D(pool_size=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(8, activation="relu"),
        tf.keras.layers.Dense(2, activation="softmax")
    ]

    classifier = tf.keras.Sequential(LAYERS)
    logging.info(f"\n<<<<<<<<<<<<<< MODEL SUMMARY >>>>>>>>>>>>>> \n{log_model_summary(classifier)}")

    path2model =os.path.join(
        config["data"]["local_dir"],
        config['data']['model_dir']
    )
    create_directories([path2model])
    path2model_dir = os.path.join(
        path2model,
        config['data']['model_file']
    )
    classifier.save(path2model_dir)
    logging.info(f"model saved at {path2model_dir}")


    classifier.compile(
        optimizer=tf.keras.optimizers.Adam(param['lr']),
        loss=param["loss"],
        metrics=param['metrics']
    )
    pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config,params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e