import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories,unzip_file
from src.utils.mdm import  val_data
import random
import urllib.request as req

STAGE = "GET DATA" ## <<< change stage name

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    ## read config files
    config = read_yaml(config_path)
    url = config["data"]["url"] #in config.yaml(it is a nested dict) find value of url(a key) in data (which is a key) and store the url

    local_dir = config["data"]["local_dir"]#get the local dirct name
    create_directories([local_dir])

    data_file= config["data"]["data_file"]
    data_file_path = os.path.join(local_dir,data_file)

    if not os.path.isfile(data_file_path):
        logging.info(">>>>>>>>>>started downloading...........")
        filename,headers = req.urlretrieve(url,data_file_path)
        logging.info(f"filename: {filename} created at \n{headers}")
    else:
        logging.info(f"file:{data_file} already present")

    unzip_data_dir = config['data']['unzip_data_dir']
    if os.path.exists(unzip_data_dir):
        logging.info(f"data ecxtraction started")
        create_directories([unzip_data_dir])
        unzip_data_dir_path = os.path.join(local_dir)
        unzip_file(source = data_file_path,dest = unzip_data_dir_path )
    else:
        logging.info(f"data already extracted")

    # validating data
    logging.info("starting validation")
    val_data(config)
    logging.info("data validation completed")






    #params = read_yaml(params_path)
    pass


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e