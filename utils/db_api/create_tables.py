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
    # CREATE TABLES + INDEXES
    # =======================
    async def create_tables(self):
        sql = """
        -- USERS
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE
        );

        -- CLIENTS
        CREATE TABLE IF NOT EXISTS clients (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            full_name VARCHAR(255) NOT NULL,
            phone VARCHAR(20),
            latitude  NUMERIC(10,6),
            longitude NUMERIC(10,6),
            created_at TIMESTAMP DEFAULT NOW()
        );

        -- SEND TABLE
        CREATE TABLE IF NOT EXISTS send_table (
            id SERIAL PRIMARY KEY,
            status BOOLEAN DEFAULT FALSE
        );

        -- =======================
        -- INDEXES
        -- =======================

        -- users.telegram_id uchun tez qidiruv
        CREATE UNIQUE INDEX IF NOT EXISTS idx_users_telegram_id
            ON users (telegram_id);

        -- clients.user_id uchun JOIN va EXISTS tezlashadi
        CREATE INDEX IF NOT EXISTS idx_clients_user_id
            ON clients (user_id);
        """

        async with self.pool.acquire() as conn:
            await conn.execute(sql)
