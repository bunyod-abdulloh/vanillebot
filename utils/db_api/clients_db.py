from utils.db_api.create_tables import Database


class ClientsDB:
    def __init__(self, db: Database):
        self.db = db

    async def add_client(self, telegram_id, full_name, phone, latitude, longitude):
        sql = """
            INSERT INTO clients (user_id, full_name, phone, latitude, longitude)
            SELECT id, $2, $3, $4, $5
            FROM users
            WHERE telegram_id = $1            
        """
        return await self.db.fetchval(
            sql,
            telegram_id,
            full_name,
            phone,
            latitude,
            longitude
        )

    async def check_client(self, telegram_id):
        sql = """
            SELECT EXISTS (
                SELECT 1
                FROM users u
                LEFT JOIN clients c ON c.user_id = u.id
                WHERE u.telegram_id = $1
                  AND c.user_id IS NOT NULL
            )
        """
        return await self.db.fetchval(sql, telegram_id)

    async def get_client(self, telegram_id):
        sql = """
            SELECT c.full_name, c.phone, c.latitude, c.longitude FROM clients c 
            JOIN users u ON c.user_id = u.id 
            WHERE u.telegram_id = $1
            """
        return await self.db.fetchrow(sql, telegram_id)

    async def set_full_name(self, full_name, telegram_id):
        sql = """
            UPDATE clients c
            SET full_name = $1
            FROM users u
            WHERE u.id = c.user_id
              AND u.telegram_id = $2
        """
        await self.db.execute(sql, full_name, telegram_id)

    async def set_phone(self, phone, telegram_id):
        sql = """
            UPDATE clients c
            SET phone = $1
            FROM users u
            WHERE u.id = c.user_id
              AND u.telegram_id = $2
        """
        await self.db.execute(sql, phone, telegram_id)

    async def set_location(self, latitude, longitude, telegram_id):
        sql = """
            UPDATE clients c
            SET latitude = $1, longitude = $2
            FROM users u
            WHERE u.id = c.user_id
              AND u.telegram_id = $3
        """
        await self.db.execute(sql, latitude, longitude, telegram_id)
