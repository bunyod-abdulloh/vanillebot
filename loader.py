from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from utils.db_api.admins import SendingDB
from utils.db_api.clients_db import ClientsDB
from utils.db_api.create_tables import Database
from utils.db_api.users import UsersDB

bot = Bot(token=config.BOT_TOKEN, parse_mode=None)
# storage = RedisStorage2(
#     host='localhost',
#     port=6379,
#     db=5,
#     state_ttl=3600,
#     data_ttl=3600,
# password=REDIS_PASS
# )
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()
udb = UsersDB(db)
sdb = SendingDB(db)
clsdb = ClientsDB(db)
