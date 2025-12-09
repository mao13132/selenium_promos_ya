# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import os
import shutil

from src.browser.clear_profile import _clean_profile_files, _remove_lock_files
from src.utils._logger import logger_msg


async def copy_profile(settings):
    backup_profile_path = settings['profile_path']

    path_chrome = settings['path_chrome']

    # Удаляем lock файлы если они есть
    _remove_lock_files(path_chrome)

    # Проверяем существование исходного профиля
    if not os.path.exists(path_chrome):
        logger_msg(f'Исходный профиль не найден: {path_chrome}')
        return True

    try:
        # Копируем профиль
        shutil.copytree(path_chrome, backup_profile_path, copy_function=shutil.copy2, dirs_exist_ok=True)

        # Удаляем потенциально проблемные файлы из скопированного профиля
        _clean_profile_files(backup_profile_path)

    except Exception as es:
        logger_msg(f'Не могу скопировать папку профиля "{es}"')
        return False

    return True

