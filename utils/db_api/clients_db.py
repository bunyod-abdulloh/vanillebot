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
                FROM client_client 
                WHERE telegram_id = $1                  
            )
        """
        return await self.db.fetchval(sql, telegram_id)

    async def get_client(self, telegram_id):
        sql = """
            SELECT full_name, phone, latitude, longitude FROM client_client            
            WHERE telegram_id = $1
            """
        return await self.db.fetchrow(sql, telegram_id)

    async def set_full_name(self, full_name, telegram_id):
        sql = """
            UPDATE client_client 
            SET full_name = $1            
            WHERE telegram_id = $2
        """
        await self.db.execute(sql, full_name, telegram_id)

    async def set_phone(self, phone, telegram_id):
        sql = """
            UPDATE client_client
            SET phone = $1            
            WHERE telegram_id = $2
        """
        await self.db.execute(sql, phone, telegram_id)

    async def set_location(self, latitude, longitude, telegram_id):
        sql = """
            UPDATE client_client
            SET latitude = $1, longitude = $2            
            WHERE telegram_id = $3
        """
        await self.db.execute(sql, latitude, longitude, telegram_id)
