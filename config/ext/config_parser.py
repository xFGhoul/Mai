import yaml
import os

from utils.logging import log

CONFIG_PATH = "config/config.yaml"

if not os.path.exists(CONFIG_PATH):
    log.error(
        "[CONFIG] CONFIG.YAML DOES NOT EXIST. PLEASE SEE => example.config.yaml"
    )
    raise SystemExit  # Realistically this won't ever be called if you run the launcher but just incase you actually did 'python mai.py' :cringe:

with open(CONFIG_PATH) as f:
    config = yaml.load(f, yaml.Loader)
