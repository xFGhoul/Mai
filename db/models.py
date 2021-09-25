import asyncio
import aioredis

from tortoise import fields
from tortoise.models import Model

from config.ext.config_parser import config


class Guild(Model):
    discord_id = fields.BigIntField(pk=True)
    language = fields.TextField(default="en")
    prefix = fields.TextField(default="-")
