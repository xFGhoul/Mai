import configparser
import os

import yaml

from utils.logging import log

ROOT_DIR = os.path.abspath(os.curdir)

CONFIG_PATH = "config/config.yaml"
INI_CONFIG_PATH = os.path.join(ROOT_DIR, "mai.ini")

if not os.path.exists(CONFIG_PATH):
    log.error(
        "[CONFIG] CONFIG.YAML DOES NOT EXIST. PLEASE SEE => example.config.yaml"
    )
    raise SystemExit  # Realistically this won't ever be called if you run the launcher but just incase you actually did 'python mai.py' :cringe:

with open(CONFIG_PATH) as f:
    config = yaml.load(f, yaml.Loader)

ini = configparser.ConfigParser()
ini.read(INI_CONFIG_PATH)
