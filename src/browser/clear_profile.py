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
import time
import glob

from settings import PATCH_PROFILES, profiles_path
from src.utils._logger import logger_msg


def clear_profile_and_create(name_profile_chrome):
    res_clear_ = _clear_profile(name_profile_chrome)

    res_create = _create_profile(name_profile_chrome)

    return True


def _clear_profile(name_profile_chrome):
    """Полная очистка и пересоздание профиля Chrome"""
    try:
        PATCH_PROFILE_CHROME = f"{PATCH_PROFILES}{os.sep}{name_profile_chrome}"

        # Удаляем lock файлы если они есть
        _remove_lock_files(PATCH_PROFILE_CHROME)

        # Удаляем старый профиль с несколькими попытками
        for attempt in range(3):
            try:
                if os.path.exists(PATCH_PROFILE_CHROME):
                    shutil.rmtree(PATCH_PROFILE_CHROME)
                break
            except Exception as es:
                if attempt == 2:  # последняя попытка
                    if 'Системе не удается найти указанный путь' not in str(es):
                        logger_msg(f'Не могу удалить папку профиля после {attempt + 1} попыток: "{es}"')
                        return False
                else:
                    time.sleep(2)  # ждем перед следующей попыткой
                    continue

        # Ждем полного удаления
        time.sleep(1)

    except Exception as es:
        logger_msg(f'Общая ошибка при очистке профиля: "{es}"')
        return False


def _create_profile(name_profile_chrome):
    """Пересоздание профиля Chrome"""
    try:
        PATCH_PROFILE_CHROME = f"{PATCH_PROFILES}{name_profile_chrome}"

        PATCH_DIR_PROFILE = f"{profiles_path}{os.sep}{name_profile_chrome}"

        # Создаем директорию если не существует
        os.makedirs(os.path.dirname(PATCH_PROFILE_CHROME), exist_ok=True)

        # Проверяем существование исходного профиля
        if not os.path.exists(PATCH_DIR_PROFILE):
            print(f'Пересоздать профиль не могу т.к. нет резервной копии по адресу: {PATCH_DIR_PROFILE}')
            return True

        try:
            # Копируем профиль
            shutil.copytree(PATCH_DIR_PROFILE, PATCH_PROFILE_CHROME, copy_function=shutil.copy2, dirs_exist_ok=True)

            # Удаляем потенциально проблемные файлы из скопированного профиля
            _clean_profile_files(PATCH_PROFILE_CHROME)

        except Exception as es:
            logger_msg(f'Не могу скопировать папку профиля "{es}"')
            return False

        logger_msg('Успешно пересоздал папку с профилем браузера')
        return True

    except Exception as es:
        logger_msg(f'Общая ошибка при пересоздании профиля: "{es}"')
        return False


def _remove_lock_files(PATCH_PROFILE_CHROME):
    """Удаляет lock файлы Chrome"""
    try:
        lock_patterns = [
            os.path.join(PATCH_PROFILE_CHROME, 'SingletonLock'),
            os.path.join(PATCH_PROFILE_CHROME, 'lockfile'),
            os.path.join(PATCH_PROFILE_CHROME, '**', 'LOCK'),
            os.path.join(PATCH_PROFILE_CHROME, '**', '*.lock'),
        ]

        for pattern in lock_patterns:
            for lock_file in glob.glob(pattern, recursive=True):
                try:
                    if os.path.exists(lock_file):
                        os.remove(lock_file)
                except Exception as es:
                    logger_msg(f'Не удалось удалить lock файл {lock_file}: {es}')

        return True

    except Exception as es:
        logger_msg(f'Ошибка при удалении lock файлов: {es}')

        return False


def _clean_profile_files(profile_path):
    """Очищает проблемные файлы из профиля"""
    try:
        # Файлы и папки которые могут вызывать проблемы
        problematic_items = [
            'SingletonLock',
            'lockfile',
            'Crash Reports',
            'chrome_debug.log',
            'Preferences.backup',
        ]

        for item in problematic_items:
            item_path = os.path.join(profile_path, item)
            try:
                if os.path.exists(item_path):
                    if os.path.isfile(item_path):
                        os.remove(item_path)
                    else:
                        shutil.rmtree(item_path)
                    logger_msg(f'Удален проблемный элемент: {item}')
            except Exception as es:
                logger_msg(f'Не удалось удалить {item}: {es}')

    except Exception as es:
        logger_msg(f'Ошибка при очистке проблемных файлов: {es}')
