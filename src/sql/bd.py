# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings import SQL_URL, Base
from src.sql.accounts import AccountsCRUD
from src.sql.tasks import TasksCRUD, Tasks

from src.utils._logger import logger_msg


class BotDB:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self):
        try:
            self.engine = create_async_engine(SQL_URL)

            self.params = {
                'class_': AsyncSession, 'expire_on_commit': False
            }

            # Создаём сессию
            self.async_session_maker = sessionmaker(self.engine, **self.params)

            self.accounts = AccountsCRUD(self.async_session_maker)

            self.tasks = TasksCRUD(self.async_session_maker)

        except Exception as es:
            error_ = f'SQL не могу создать подключение "{es}"'

            logger_msg(error_)

    async def init_bases(self):
        try:
            async with self.engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

                return True
        except Exception as es:
            error_ = f'SQL Postgres: Ошибка не могу подключиться к базе данных "{es}"\n' \
                     f'"{SQL_URL}"'

            logger_msg(error_)

            return False
