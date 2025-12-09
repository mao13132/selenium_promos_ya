# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time
import os

from src.browser.clear_profile import clear_profile_and_create
from src.browser.close_old_chrome_process import close_old_chrome_process
from src.browser.createbrowser_uc import CreatBrowser
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def create_browser_profile(path_chrome, name_profile_chrome, path_short_chrome):
    error = ''

    for _try in range(3):
        try:

            if _try > 0 or not _is_profile_healthy(path_chrome):
                print(f"Попытка {_try + 1}: Пересоздаю профиль")
                if not clear_profile_and_create(name_profile_chrome):
                    logger_msg("Не удалось очистить профиль, пропускаю попытку")
                    time.sleep(5)
                    continue

                time.sleep(2)

            browser = CreatBrowser(path_short_chrome, name_profile_chrome)
            
            return browser

        except Exception as es:
            error = f'⚠️⚠️⚠️ Ошибка создания браузера "{es}"\n\nПопытка "{_try + 1}"'

            if 'This version of ChromeDriver only supports' in str(es):

                error_ = f'Не могу запустить браузер! Обновите версию Chrome на сервере'

                logger_msg(error_)

                SendlerOneCreate('').save_text(error_)

                return False
            
            # Полная очистка при ошибках подключения
            if any(keyword in str(es).lower() for keyword in 
                   ['cannot connect to chrome', 'chrome not reachable', 'session not created']):
                logger_msg("Обнаружена ошибка подключения к Chrome, выполняю полную очистку")
                close_old_chrome_process(['chrome.exe', 'chromedriver.exe'])
                time.sleep(3)
                clear_profile_and_create(name_profile_chrome)
                time.sleep(5)
            else:
                time.sleep(10)
            
            continue

    logger_msg("Не удалось создать браузер после 3 попыток")

    logger_msg(error)
    SendlerOneCreate('').save_text(f'WB DDR: {error}')
    return False


def _is_profile_healthy(path_chrome):
    """Проверяет здоровье профиля Chrome"""
    try:
        if not os.path.exists(path_chrome):
            print(f'Учетной записи браузера "{path_chrome}" не существует в системе! Создаю...')
            return False
            
        # Проверяем наличие lock файлов
        lock_files = [
            os.path.join(path_chrome, 'SingletonLock'),
            os.path.join(path_chrome, 'lockfile'),
        ]
        
        for lock_file in lock_files:
            if os.path.exists(lock_file):
                logger_msg(f"Найден lock файл: {lock_file}")
                return False
                
        return True
        
    except Exception as es:
        logger_msg(f"Ошибка при проверке здоровья профиля: {es}")
        return False
