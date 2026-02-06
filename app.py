import middlewares, filters, handlers

from aiogram import executor

from loader import dp, db

from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands


async def on_startup(dispatcher):
    await set_default_commands(dispatcher)
    await on_startup_notify(dispatcher)
    await db.create()
    # await udb.drop_table_users()
    # await tstdb.drop_table_tests()
    # await scsdb.drop_table_sciences()
    # await utadb.drop_table_uta()
    # await scrsdb.drop_table_scores()
    await db.create_tables()
    # await udb.add_user(
    #     telegram_id=int(6572090778), full_name="Bekzod Jo'rayev"
    # )



if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True, allowed_updates=["message", "callback_query",
                                                                                          "chat_member"])
