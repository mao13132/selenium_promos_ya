# ---------------------------------------------
# Program by @developer_telegrams
# Task Monitoring System
#
# Version   Date        Info
# 1.0       2023    Initial Version
# 2.0       2024    Task Monitor Implementation
# 3.0       2025    Auto Task Creator Integration
#
# ---------------------------------------------
import asyncio

from src.business.tasks.promo_work.promo_work import PromoWork
from src.business.tasks_wait.monitoring_task import TaskMonitor
from src.business.create_auto_task.auto_task_creator import AutoTaskCreator


class StartWaitTasks:
    """Основной класс для работы с задачами"""

    def __init__(self, settings):
        self.settings = settings
        self.BotDB = settings['BotDB']
        self.monitor = TaskMonitor(check_interval=5, BotDB=settings['BotDB'])
        self.auto_creator = AutoTaskCreator(self.BotDB)
        self._setup_task_handlers()

    def _setup_task_handlers(self):
        """Настройка обработчиков задач"""
        self.monitor.register_task_handler("change_promo", PromoWork(self.settings, mode="change_promo").start_work)

    async def start_wait(self):
        # Запуск авто‑создателя задач в фоне
        asyncio.create_task(self.auto_creator.run_loop())
        # Запуск мониторинга задач
        await self.monitor.start_monitoring()
