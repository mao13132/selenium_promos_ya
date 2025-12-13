# ---------------------------------------------
# Program by @developer_telegrams
# Авто‑создание задач по расписанию
#
# Version   Date        Info
# 1.0       2025    Initial Version
# ---------------------------------------------
import asyncio
import json

from settings import TIME_KEY_SCHEDULE, ADMIN
from src.utils._logger import logger_msg


class AutoTaskCreator:
    """Периодически создает задачи по всем магазинам"""

    def __init__(self, BotDB, default_minutes=10):
        self.BotDB = BotDB
        self.default_minutes = default_minutes
        self._is_running = False

    async def _get_interval_minutes(self):
        """Получить интервал в минутах из таблицы настроек"""
        try:
            # Инициализируем настройку, если её нет
            await self.BotDB.settings.start_settings(
                key=TIME_KEY_SCHEDULE,
                value=str(self.default_minutes),
                types='int'
            )
        except Exception as es:
            logger_msg(f'AutoTaskCreator: ошибка init settings "{es}"')

        value = await self.BotDB.settings.get_setting(TIME_KEY_SCHEDULE)
        try:
            minutes = int(value)
            return minutes if minutes > 0 else self.default_minutes
        except Exception:
            return self.default_minutes

    async def _create_tasks_for_all_shops(self):
        """Создать задачи для всех магазинов"""
        try:
            shops = await self.BotDB.shops.read_all()
        except Exception as es:
            logger_msg(f'AutoTaskCreator: не удалось прочитать магазины "{es}"')
            return

        created = 0
        for shop in shops or []:
            try:
                params = {'cabinet': shop.name, 'percent_list': shop.percent_values}
                payload = {
                    'title': 'Задача изменения промо',
                    'description': 'Автозапуск процесса change_promo',
                    'task_type': 'change_promo',
                    'shop_id': int(shop.id_pk),
                    'created_by_user_id': str(ADMIN),
                    'parameters': json.dumps(params, ensure_ascii=False),
                }
                task_id = await self.BotDB.tasks.create(payload)
                created += 1 if task_id else 0
            except Exception as es:
                logger_msg(
                    f'AutoTaskCreator: ошибка создания задачи для магазина "{getattr(shop, "name", "")}": "{es}"')
                continue

            continue

        logger_msg(f'AutoTaskCreator: создано задач {created} из {len(shops or [])}')

    async def run_loop(self):
        """Основной бесконечный цикл создания задач"""
        self._is_running = True
        while self._is_running:
            minutes = await self._get_interval_minutes()
            await self._create_tasks_for_all_shops()
            await asyncio.sleep(int(minutes) * 60)

    def stop(self):
        """Остановить цикл"""
        self._is_running = False
