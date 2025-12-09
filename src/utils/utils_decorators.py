# utils_decorators.py
import sys
import traceback
import inspect
from functools import wraps
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def catch_and_report(prefix: str):
    """
    Асинхронный декоратор: единообразно перехватывает исключения, пишет лог и возвращает False.
    """
    def deco(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as es:
                error_ = f'{prefix}: {es}'
                logger_msg(
                    f"{error_}\n"
                    f"{''.join(traceback.format_exception(sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2]))}"
                )
                SendlerOneCreate('').save_text(error_)
                return False
        return wrapper
    return deco
    