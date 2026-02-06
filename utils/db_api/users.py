from utils.db_api.create_tables import Database


class UsersDB:
    def __init__(self, db: Database):
        self.db = db
        
    async def add_user(self, telegram_id, full_name, phone_number):
        sql = "INSERT INTO users (telegram_id, full_name, phone_number) VALUES ($1, $2, $3) ON CONFLICT (telegram_id) DO NOTHING"
        await self.db.execute(sql, telegram_id, full_name, phone_number)

    async def check_user(self, telegram_id):
        sql = "SELECT EXISTS (SELECT 1 FROM users WHERE telegram_id = $1)"
        return await self.db.fetchval(sql, telegram_id)

    async def get_user(self, telegram_id):
        sql = "SELECT * FROM users WHERE telegram_id = $1"
        return await self.db.fetchrow(sql, telegram_id)

    async def select_all_users(self):
        sql = "SELECT telegram_id FROM users"
        return await self.db.fetch(sql)

    async def select_users_offset(self, offset: int = 0, limit: int = 1000):
        sql = "SELECT telegram_id FROM users ORDER BY id LIMIT $1 OFFSET $2"
        return await self.db.fetch(sql, limit, offset)

    async def set_full_name(self, telegram_id, full_name):
        sql = "UPDATE users SET full_name = $1 WHERE telegram_id = $2"
        return await self.db.execute(sql, full_name, telegram_id)

    async def set_phone_number(self, telegram_id, phone_number):
        sql = "UPDATE users SET phone_number = $1 WHERE telegram_id = $2"
        return await self.db.execute(sql, phone_number, telegram_id)

    async def count_users(self):
        sql = "SELECT COUNT(id) FROM users"
        return await self.db.fetchval(sql)

    async def delete_user(self, telegram_id):
        sql = "DELETE FROM users WHERE telegram_id = $1"
        return await self.db.execute(sql, telegram_id)
