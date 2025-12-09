# ---------------------------------------------
# Program by @developer_telegrams
# Task Monitoring System
#
# Version   Date        Info
# 1.0       2023    Initial Version
# 2.0       2024    Task Monitor Implementation
#
# ---------------------------------------------

from src.business.tasks_wait.monitoring_task import TaskMonitor


class StartWaitTasks:
    """Основной класс для работы с задачами"""

    def __init__(self, settings):
        self.settings = settings
        self.BotDB = settings['BotDB']
        self.monitor = TaskMonitor(check_interval=5, BotDB=settings['BotDB'])
        self._setup_task_handlers()

    def _setup_task_handlers(self):
        """Настройка обработчиков задач"""
        self.monitor.register_task_handler("change_promo", PromoWork(self.settings, mode="change_promo").start_work)

    async def start_wait(self):
        await self.monitor.start_monitoring()
