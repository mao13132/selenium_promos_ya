# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
from typing import Callable

from src.business.tasks_wait.dispatcher_task import TaskDispatcher
from src.utils._logger import logger_msg


class TaskMonitor:
    """Монитор задач - проверяет БД и запускает выполнение"""

    def __init__(self, check_interval, BotDB):
        self.BotDB = BotDB
        self.check_interval = check_interval  # Интервал проверки в секундах
        self.dispatcher = TaskDispatcher(BotDB)
        self.is_running = False

    def register_task_handler(self, task_type: str, handler: Callable):
        """Регистрация обработчика задачи"""
        self.dispatcher.register_handler(task_type, handler)

    async def check_and_process_tasks(self):
        """Проверка и обработка задач из БД"""
        try:
            # Получаем задачи в ожидании
            pending_tasks = await self.BotDB.tasks.get_pending_tasks()

            if not pending_tasks:
                return

            print(f"Найдено {len(pending_tasks)} задач для выполнения")

            # Обрабатываем каждую задачу
            for task in pending_tasks:
                await self.dispatcher.dispatch_task(task)

                continue

        except Exception as e:
            logger_msg(f"Ошибка при проверке задач: {e}")

    async def start_monitoring(self):
        """Запуск мониторинга задач"""
        self.is_running = True

        print(f'Ожидаю задачи...')

        while self.is_running:
            await self.check_and_process_tasks()
            await asyncio.sleep(self.check_interval)

    def stop_monitoring(self):
        """Остановка мониторинга"""
        self.is_running = False
        logger_msg("Мониторинг задач остановлен")
