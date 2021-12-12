"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""

import asyncio
import aioredis

from discord import Guild as GuildModel
from discord.ext.commands import Context


from tortoise import fields
from tortoise.expressions import F
from tortoise.models import Model

from config.ext.parser import config

aioredis.util._converters[bool] = lambda x: b"1" if x else b"0"
redis: aioredis.Redis


async def connect_redis():
    global redis

    redis = aioredis.Redis(
        await aioredis.create_connection(config["REDIS_URI"])
    )


asyncio.ensure_future(connect_redis())


def from_redis_hash(cls, hashmap: dict):
    return {
        k: v == "1"
        if isinstance(cls._meta.fields_map[k], fields.BooleanField)
        else v
        for k, v in hashmap.items()
    }


def redis_hashmap(instance):
    return {
        k: getattr(instance, k)
        for k in instance._meta.db_fields
        if getattr(instance, k) != None
    }


async def c_save(obj, update_fields=[]):
    redis_hashmap(obj)
    await asyncio.wait([c(obj) for c in obj.__cache_updaters])
    await obj.save(update_fields=update_fields)


def cached_model(*, key: str):
    def predicate(cls: type):
        nonlocal key

        if not hasattr(cls, "__cache_updaters"):
            cls.__cache_updaters = []

        async def c_get_or_create(cls=cls, cached_key=None, **kwargs):
            cached = await c_get_from_cache(cached_key)
            if cached:
                return cls(**from_redis_hash(cls, cached)), False

            obj, created = await cls.get_or_create(
                **{key: cached_key}, **kwargs
            )
            await c_update_cache(obj)
            return obj, created

        async def c_get_or_none(cls=cls, cached_key=None, **kwargs):
            cached = await c_get_from_cache(cached_key)
            if cached:
                return cls(**from_redis_hash(cls, cached))

            obj = await cls.get_or_none(**{key: cached_key}, **kwargs)
            if obj is not None:
                await c_update_cache(obj)
            return obj

        async def c_get(cls=cls, cached_key=None, **kwargs):
            cached = await c_get_from_cache(cached_key)
            if cached:
                return cls(**from_redis_hash(cls, cached))

            obj = await cls.get(**{key: cached_key}, **kwargs)
            await c_update_cache(obj)
            return obj

        async def c_get_from_cache(value):
            return await redis.hgetall(
                f"{cls.__name__};{key};{value}", encoding="utf-8"
            )

        async def c_update_cache(obj):
            await redis.hmset_dict(
                f"{cls.__name__};{key};{getattr(obj, key)}", redis_hashmap(obj)
            )

        cls.__cache_updaters.append(c_update_cache)

        cleankey = key.replace("__", "_")

        # Internal methods added for possible use cases
        setattr(cls, "c_update_cache_by_" + cleankey, c_update_cache)
        setattr(cls, "c_get_from_cache_by_" + cleankey, c_get_from_cache)

        # The save method
        setattr(cls, "c_save", c_save)

        # The classmethods
        setattr(
            cls, "c_get_or_create_by_" + cleankey, classmethod(c_get_or_create)
        )
        setattr(cls, "c_get_or_none_by_" + cleankey, classmethod(c_get_or_none))
        setattr(cls, "c_get_by_" + cleankey, classmethod(c_get))
        return cls

    return predicate


@cached_model(key="discord_id")
class Guild(Model):
    # Core Components Of The Model
    discord_id = fields.BigIntField(pk=True)
    language = fields.TextField(default="en")
    prefix = fields.TextField(default="-")
    timezone = fields.TextField(default="UTC")

    changelog_enabled = fields.BooleanField(default=False)
    changelog_channel = fields.BigIntField(default=None, null=True)

    trusted_bot_owners = fields.BigIntField(null=True)

    # Some Checks (soon™)
    is_bot_blacklisted = fields.BooleanField(default=False)
    blacklisted_reason = fields.TextField(default="Violating TOS", unique=False)
    is_premium = fields.BooleanField(default=False)

    # Some Fields When Doing Global Checks (soon™)
    blacklisted_channels = fields.BigIntField(null=True)

    @classmethod
    async def from_id(cls, guild_id):
        # TODO: Implement caching in here or override get method
        return (await cls.get_or_create(discord_id=guild_id))[0]

    @classmethod
    async def from_guild_object(cls, guild: GuildModel):
        return await cls.from_id(guild.id)

    @classmethod
    async def from_context(cls, ctx: Context):
        return await cls.from_id(ctx.guild.id)


class OSU(Model):
    id = fields.BigIntField(pk=True)
    username = fields.TextField(default=None, unqiue=False)
    skin = fields.TextField(default="Default Skin", unique=False)
    passive = fields.BooleanField(default=True)
    discord_id = fields.BigIntField()
    guild = fields.ForeignKeyField("Mai.Guild", related_name="OSU")


class AFKModel(Model):
    id = fields.BigIntField(pk=True)
    afk_user_id = fields.BigIntField()
    start_time = fields.DatetimeField(auto_now_add=True)
    enabled = fields.BooleanField(default=True)
    nickname = fields.TextField(default=None, null=True)
    message = fields.TextField(default=None, null=True)
    guild = fields.ForeignKeyField("Mai.Guild", related_name="AFK")


class Snipe(Model):
    id = fields.BigIntField(pk=True)
    enabled = fields.BooleanField(default=True)
    guild = fields.ForeignKeyField("Mai.Guild", related_name="Snipe")


class Captcha(Model):
    id = fields.BigIntField(pk=True)
    enabled = fields.BooleanField(default=False)
    guild = fields.ForeignKeyField("Mai.Guild", related_name="Captcha")
    type = fields.TextField(
        default="text"
    )  # Types: Audio, Text, Picture, Arithimetic


class Counting(Model):
    discord_id = fields.BigIntField(pk=True)
    guild = fields.ForeignKeyField("Mai.Guild", related_name="Counting")
    counting_channel = fields.BigIntField(null=True)
    counting_goal = fields.BigIntField(default=0, null=True)
    counting_number = fields.BigIntField(default=0, null=True)
    counting_warn_message = fields.TextField(
        default="Please use this channel for counting only!", null=True
    )
    enabled = fields.BooleanField(default=True)
    last_member_id = fields.BigIntField(null=True)
    webhook_url = fields.CharField(null=True, max_length=400)

    async def increment(self, increase_no: int = 1):
        self.counting_number = F("counting_number") + increase_no
        await self.save(update_fields=["counting_number"])
        await self.refresh_from_db(fields=["counting_number"])
        return self.counting_number

    @property
    def next_number(self):
        return self.counting_number + 1


class ServerLogging(Model):
    id = fields.BigIntField(pk=True)
    # Main Fields
    guild = fields.ForeignKeyField("Mai.Guild", related_name="Logging")
    channel_id = fields.BigIntField(default=None, null=True)
    enabled = fields.BooleanField(default=True)

    # Optional Fields
    log_actions_by_bots = fields.BooleanField(default=True)
    ignored_logging_channels = fields.BigIntField(default=None, null=True)

    # Logging Types

    # Message Events
    message_edited = fields.BooleanField(default=True)
    message_deleted = fields.BooleanField(default=True)

    # Member Events
    nickname_changed = fields.BooleanField(default=True)
    member_updated = fields.BooleanField(default=True)

    member_banned = fields.BooleanField(default=True)
    member_unbanned = fields.BooleanField(default=True)

    member_joined = fields.BooleanField(default=True)
    member_left = fields.BooleanField(default=True)

    # Role Events
    role_created = fields.BooleanField(default=True)
    role_updated = fields.BooleanField(default=True)
    role_deleted = fields.BooleanField(default=True)

    member_roles_changed = fields.BooleanField(default=True)

    # Voice Events
    member_joined_voice_channel = fields.BooleanField(default=True)
    member_left_voice_channel = fields.BooleanField(default=True)

    # Server Events

    server_edited = fields.BooleanField(default=True)

    server_emojis_updated = fields.BooleanField(default=True)

    # Channel Events

    channel_created = fields.BooleanField(default=True)
    channel_updated = fields.BooleanField(default=True)
    channel_deleted = fields.BooleanField(default=True)

    # Invite Events
    invite_created = fields.BooleanField(default=True)
    invite_deleted = fields.BooleanField(default=True)
