from typing import Optional

import asyncpg
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Optional[Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            min_size=1,
            max_size=10
        )

    # =======================
    # QUERY METHODS
    # =======================
    async def fetch(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetch(query, *args)

    async def fetchrow(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchrow(query, *args)

    async def fetchval(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.fetchval(query, *args)

    async def execute(self, query, *args):
        async with self.pool.acquire() as conn:
            return await conn.execute(query, *args)

    # =======================
    # CREATE TABLES
    # =======================
    async def create_tables(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE NOT NULL,            
            full_name VARCHAR(255) NOT NULL,
            phone_number VARCHAR(20) NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );

        CREATE TABLE IF NOT EXISTS send_table (
            id SERIAL PRIMARY KEY,
            status BOOLEAN DEFAULT FALSE
        );        
        """

        async with self.pool.acquire() as conn:
            await conn.execute(sql)
