# ---------------------------------------------
# Program by @developer_telegrams
# Фабрика фейковой задачи для запуска без БД
# ---------------------------------------------
import json
from typing import Dict, Any

from settings import ADMIN
from src.sql.tasks import Tasks, TaskStatus

# Конфиг фейковой задачи — изменяйте параметры под свои нужды
FAKE_TASK_CONFIG: Dict[str, Any] = {
    "id_pk": 999999,  # Идентификатор, не используется в БД
    "title": "Фейковая задача изменения промо",
    "description": "Запуск процесса change_promo без записи в БД",
    "task_type": "change_promo",  # Должен совпадать с зарегистрированным обработчиком
    "shop_id": 1,  # Укажите существующий ID магазина в вашей БД
    "created_by_user_id": str(ADMIN),  # Telegram ID инициатора
    "parameters": {
        "cabinet": "Я.Store",
        "cabinet_id": "216275410",
        "percent_list": "[0, 1, 2, 3]"
    },
}


def build_fake_task() -> Tasks:
    """Собирает объект Tasks на основе конфига без записи в БД"""
    cfg = FAKE_TASK_CONFIG

    task = Tasks()
    task.id_pk = cfg["id_pk"]
    task.title = cfg["title"]
    task.description = cfg["description"]
    task.task_type = cfg["task_type"]
    task.shop_id = cfg["shop_id"]
    task.status = TaskStatus.PENDING
    task.result = None
    task.error_message = None
    task.parameters = json.dumps(cfg["parameters"])  # Преобразуем dict в JSON-строку
    task.created_by_user_id = str(cfg["created_by_user_id"])
    task.started_at = None
    task.completed_at = None
    task.created_at = None
    task.updated_at = None
    task.is_active = True

    return task
