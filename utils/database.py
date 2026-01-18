"""

███╗   ███╗ █████╗ ██╗
████╗ ████║██╔══██╗██║
██╔████╔██║███████║██║
██║╚██╔╝██║██╔══██║██║
██║ ╚═╝ ██║██║  ██║██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝

Made With ❤️ By Ghoul & Nerd

"""
import asyncpg
import asyncio

from typing import Optional, Any
from asyncpg import Pool, cursor

from config.ext import config
from utils.logging import logger

class MaiDB:
    def __init__(self) -> None:
        self.pool: Optional[Pool] = None
        self.timeout: int = 30
        
    async def initialize_pool(self, bot_loop) -> None:
        logger.info("Initializing Database Pool")
        self.pool = await asyncpg.create_pool(config["DATABASE_URI"], loop=bot_loop)
        logger.info("Initialized PostgreSQL Database Pool")
        
    async def cleanup(self) -> None:
        if self.pool:
            logger.info("Closing PostgreSQL Pool...")
            await asyncio.wait_for(self.pool.close(), timeout=10)
            logger.info("Closed PostgreSQL Pool")
            
    async def fetch(self, sql: str, params) -> str:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.fetch(sql, params)
                    return data
                
    async def execute(self, sql: str, *params) -> str:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.execute(sql, *params)
                    return data
                
    async def fetchrow(self, sql: str, params) -> str:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.fetchrow(sql, params)
                    return data
    
    async def fetchval(self, sql: str, params) -> str:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.fetchval(sql, params)
                    return data
                
    async def create_table(self, table: str, columns: str) -> None:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.execute(f"CREATE TABLE IF NOT EXISTS {table} ( {columns} )")
                    return data
                
    async def add_column(self, table: str, column: str, type: str) -> None:
        if self.pool:
            connection: asyncpg.Connection
            async with self.pool.acquire(timeout=self.timeout) as connection:
                async with connection.transaction():
                    data = await connection.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type}")
                    return data
                
    