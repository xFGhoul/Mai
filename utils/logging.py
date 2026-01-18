"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""
import logging
import os

from loguru import logger
from typing import Dict

from .constants import Logging

def setup_logger():
    # init first log file
    if not os.path.isfile("logs/ext/[Dependencies].log"):
        # we have to make the logs dir before we log to it
        if not os.path.exists("logs"):
            os.makedirs("logs")
        open("logs/ext/[Dependencies].log", "w+")

    # set logging levels for various libs
    logging.getLogger("websockets").setLevel(logging.INFO)
    logging.getLogger("asyncpg").setLevel(logging.INFO)
    logging.getLogger("asyncio").setLevel(logging.INFO)
    logging.getLogger("rich").setLevel(logging.INFO)
    logging.getLogger("aiocache").setLevel(logging.INFO)
    
    # we want out logging formatted like this everywhere
    fmt = logging.Formatter(
        "{asctime} [{levelname}] {name}: {message}",
        datefmt="%Y-%m-%d %H:%M:%S",
        style="{",
    )

    file = logging.FileHandler(
        "logs/ext/[Dependencies].log", mode="w", encoding="utf-8"
    )
    file.setFormatter(fmt)
    file.setLevel(logging.INFO)

    # get the __main__ logger and add handlers
    root = logging.getLogger()
    root.setLevel("DEBUG")
    root.addHandler(file)

    return logging.getLogger(__name__)

discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='logs/discord/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
discord_logger.addHandler(handler)

LOGGING_CONFIG: Dict = {
    "handlers": [
        {
            "sink": Logging.MAI_LOGS_PATH,
            "format": "[{time:YYYY-MM-DD HH:mm:ss}] {module}::{function}({line}) - {message}",
            "enqueue": True,
            "rotation": "daily",
            "mode": "w",
            "level": "INFO",
            "serialize": False,
            "backtrace": False,
            "catch": False,
            },
        ],
        }
logger.configure(**LOGGING_CONFIG)
logger = logger