# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import sys
import traceback
from typing import Dict, Callable

from settings import MOKE_EDIT_TASK
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


class TaskDispatcher:
    """Диспетчер задач - распределяет задачи по типам"""

    def __init__(self, BotDB):
        self.BotDB = BotDB
        # Словарь: тип_задачи -> функция_обработчик
        self.handlers: Dict[str, Callable] = {}

    def register_handler(self, task_type: str, handler: Callable):
        """Регистрация обработчика для типа задачи"""
        self.handlers[task_type] = handler

    async def dispatch_task(self, task):
        """Отправка задачи на выполнение"""
        handler = self.handlers.get(task.task_type)
        if not handler:
            error_msg = f"Нет обработчика для типа задачи: {task.task_type}"
            logger_msg(error_msg)
            await self.BotDB.tasks.fail_task(task.id_pk, error_msg)
            return False

        id_client = task.created_by_user_id
        try:
            if not MOKE_EDIT_TASK:
                await self.BotDB.tasks.start_task(task.id_pk)
            print(f"Запущена задача ID: {task.id_pk}, тип: {task.task_type}")
            for attempt in range(1, 4):
                try:
                    result = await handler(task)

                    if not result:
                        error_msg = f"Не выполнилась задача {task.id_pk} (попытка {attempt})"
                        logger_msg(
                            f"{error_msg}\n"
                            f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}"
                        )
                        if attempt == 3:
                            if not MOKE_EDIT_TASK:
                                await self.BotDB.tasks.fail_task(task.id_pk, error_msg)
                            SendlerOneCreate('').send_msg_by_id(error_msg, id_client)
                            return False
                        continue

                    if not MOKE_EDIT_TASK:
                        await self.BotDB.tasks.complete_task(task.id_pk, str(result))

                    msg = f"Завершена задача ID: {task.id_pk}"
                    print(msg)
                    return True
                except Exception as e:
                    error_msg = f"Ошибка выполнения задачи {task.id_pk} (попытка {attempt}): {e}"
                    logger_msg(
                        f"{error_msg}\n"
                        f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}"
                    )
                    if attempt == 3:
                        if not MOKE_EDIT_TASK:
                            await self.BotDB.tasks.fail_task(task.id_pk, error_msg)
                        SendlerOneCreate('').send_msg_by_id(error_msg, id_client)
                        return False
                    continue
        except Exception as e:
            error_msg = f"Ошибка запуска задачи {task.id_pk}: {e}"
            logger_msg(
                f"{error_msg}\n"
                f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}"
            )
            if not MOKE_EDIT_TASK:
                await self.BotDB.tasks.fail_task(task.id_pk, error_msg)
            SendlerOneCreate('').send_msg_by_id(error_msg, id_client)
            return False
