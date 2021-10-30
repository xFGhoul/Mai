from config.ext.config_parser import config

TORTOISE_CONFIG = {
    "connections": {"default": config["DATABASE_URI"]},
    "apps": {
        "Mai": {
            "models": ["db.models", "aerich.models"],
            "default_connection": "default",
        }
    },
}
