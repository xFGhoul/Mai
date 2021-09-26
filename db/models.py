import asyncio
import aioredis

from tortoise import fields
from tortoise.models import Model

from discord import Guild as GuildModel
from discord.ext.commands import Context

from config.ext.config_parser import config

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
    discord_id = fields.BigIntField(pk=True)
    language = fields.TextField(default="en")
    prefix = fields.TextField(default="-")

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
