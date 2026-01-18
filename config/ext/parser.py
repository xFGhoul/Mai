"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import os

import yaml

from utils.logging import logger
from utils.constants import MAI

CONFIG_PATH = f"{MAI.ROOT_DIR}/config/config.yaml"

if not os.path.exists(CONFIG_PATH):
    logger.error(
        "[CONFIG] CONFIG.YAML DOES NOT EXIST. PLEASE SEE => config/example.config.yaml"
    )
    raise SystemExit

with open(CONFIG_PATH) as f:
    config = yaml.load(f, yaml.Loader)
