# ---------------------------------------------
# Program by @developer_telegrams
# Фабрика фейкового аккаунта для запуска без БД
# ---------------------------------------------
from typing import Dict, Any, Optional

from settings import CHROME_PROFILE
from src.sql.accounts import Accounts

# Конфиг фейкового аккаунта — изменяйте параметры под свои нужды
FAKE_ACCOUNT_CONFIG: Dict[str, Any] = {
    "id_pk": 1,
    "name": "Тестовый Аккаунт",
    "login": "+79990000000",
    "status": True,
    "status_text": None,
    "chrome_profile": CHROME_PROFILE,
    "auth_status": True,
}


def build_fake_account(account_id: Optional[int] = None) -> Accounts:
    """Собирает объект Accounts на основе конфига без записи в БД"""
    cfg = FAKE_ACCOUNT_CONFIG.copy()

    if account_id is not None:
        cfg["id_pk"] = account_id

    acc = Accounts()
    acc.id_pk = cfg["id_pk"]
    acc.name = cfg["name"]
    acc.login = cfg["login"]
    acc.status = cfg["status"]
    acc.status_text = cfg["status_text"]
    acc.chrome_profile = cfg["chrome_profile"]
    acc.auth_status = cfg["auth_status"]
    acc.created_at = None
    acc.updated_at = None

    return acc
