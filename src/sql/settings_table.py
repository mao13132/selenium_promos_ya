# ---------------------------------------------
# Program by @developer_telegrams
# Настройки: модель и CRUD
# ---------------------------------------------
from sqlalchemy import Column, Integer, String, select, insert, update

from settings import Base

from src.utils._logger import logger_msg


class Settings(Base):
    """Глобальные настройки (ключ-значение)"""
    __tablename__ = 'settings'

    id_pk = Column(Integer, primary_key=True, nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)
    types = Column(String, nullable=True)


class SettingsCRUD:
    """CRUD-операции для таблицы настроек"""

    def __init__(self, session_maker):
        self.session_maker = session_maker

    async def get_setting(self, key):
        """Получить значение настройки по ключу"""
        try:
            async with self.session_maker() as session:
                query = select(Settings).where(Settings.key == str(key))
                response = await session.execute(query)
                result = response.scalars().first()
                return result.value if result else False
        except Exception as es:
            error_ = f'SQL SettingsCRUD.get_setting: "{es}" "{key}"'
            logger_msg(error_)
            return False

    async def update_settings(self, key, value):
        """Создать или обновить настройку"""
        try:
            async with self.session_maker() as session:
                query = select(Settings).where(Settings.key == str(key))
                response = await session.execute(query)
                existing_setting = response.scalar_one_or_none()

                if existing_setting:
                    query = update(Settings).where(Settings.key == str(key)).values(value=value)
                    await session.execute(query)
                else:
                    insert_data = {
                        'key': str(key),
                        'value': value
                    }
                    query = insert(Settings).values(**insert_data)
                    await session.execute(query)

                await session.commit()
                return True
        except Exception as es:
            error_ = f'SQL SettingsCRUD.update_settings: "{es}"'
            logger_msg(error_)
            return False

    async def start_settings(self, **filters):
        """Инициализировать настройку, если её нет"""
        try:
            async with self.session_maker() as session:
                query = select(Settings).filter_by(key=filters['key'])
                response = await session.execute(query)
                exists = response.scalar_one_or_none()

                if not exists:
                    query = insert(Settings).values(**filters)
                    await session.execute(query)
                    await session.commit()

                return exists
        except Exception as es:
            error_ = f'Ошибка SQL SettingsCRUD.start_settings: "{es}"'
            logger_msg(error_)
            return False
