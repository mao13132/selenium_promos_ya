# ---------------------------------------------
# Program by @developer_telegrams
# Business Logic with Task Monitoring
#
# Version   Date        Info
# 1.0       2023    Initial Version
# 2.0       2024    Task Monitor Integration
#
# ---------------------------------------------
import asyncio

from settings import NAME_PRODUCT
from src.business.tasks_wait.start_wait_tasks import StartWaitTasks


class StartBusiness:
    """Основной бизнес-класс с интеграцией мониторинга задач"""

    def __init__(self, settings):
        self.settings = settings
        self.BotDB = settings['BotDB']
        self.name_product = NAME_PRODUCT
        self.task_monitor = StartWaitTasks(settings)

    async def start_business(self):
        res_wait = await self.task_monitor.start_wait()

        return res_wait
