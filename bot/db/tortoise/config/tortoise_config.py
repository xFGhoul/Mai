from config.ext.config_parser import config

TORTOISE_CONFIG = {
    "connections": {"default": config["DATABASE_URI"]},
    "apps": {
        config["TORTOISE_APP_NAME"]: {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
