import os

import yaml

from helpers.logging import log

ROOT_DIR = os.path.abspath(os.curdir)

CONFIG_PATH = "config/config.yaml"

if not os.path.exists(CONFIG_PATH):
    log.error(
        "[CONFIG] CONFIG.YAML DOES NOT EXIST. PLEASE SEE => example.config.yaml"
    )
    raise SystemExit

with open(CONFIG_PATH) as f:
    config = yaml.load(f, yaml.Loader)
