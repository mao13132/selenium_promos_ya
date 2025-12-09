# ---------------------------------------------
# Program by @developer_telegrams
# Force Session Save Module
#
# Модуль для принудительного сохранения сессии браузера
# через переключение вкладок. Это необходимо для корректного
# сохранения данных авторизации Google в Chrome.
#
# Version   Date        Info
# 1.0       2024        Initial Version
# ---------------------------------------------

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def force_save_session(driver, original_url: str) -> bool:
    """
    Принудительно сохраняет сессию браузера через переключение вкладок.
    
    Алгоритм:
    1. Открывает новую вкладку с Google
    2. Ждет полной загрузки
    3. Переключается на первую вкладку
    4. Сохраняет URL и закрывает первую вкладку
    5. Переключается на оставшуюся вкладку
    6. Ждет 3 секунды и открывает сохраненный URL
    
    Args:
        driver: WebDriver instance
        original_url (str): URL который нужно восстановить после процедуры
        
    Returns:
        bool: True если операция прошла успешно, False в случае ошибки
    """
    try:
        # Сохраняем текущий URL (на случай если он отличается от переданного)
        current_url = driver.current_url
        saved_url = original_url if original_url else current_url

        # Получаем handle первой вкладки
        original_window = driver.current_window_handle

        # Открываем новую вкладку с Google
        driver.switch_to.new_window("tab")
        driver.get("https://www.google.com")

        # Ждем появления новой вкладки
        WebDriverWait(driver, 10).until(lambda d: len(d.window_handles) > 1)

        # Переключаемся на новую вкладку
        new_window = None
        for handle in driver.window_handles:
            if handle != original_window:
                new_window = handle
                break

        if not new_window:
            error_ = f'Не удалось найти новую вкладку'
            logger_msg(error_)
            return False

        driver.switch_to.window(new_window)

        # Ждем загрузки Google (проверяем наличие поисковой строки)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )

        # Переключаемся обратно на первую вкладку
        driver.switch_to.window(original_window)

        # Сохраняем URL и закрываем первую вкладку
        driver.close()

        # Переключаемся на оставшуюся вкладку (Google)
        driver.switch_to.window(new_window)

        # Ждем 3 секунды для принудительного сохранения сессии
        time.sleep(10)

        # Открываем сохраненный URL
        driver.switch_to.new_window("tab")
        driver.get(saved_url)

        # Ждем загрузки страницы
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        time.sleep(10)

        return True

    except Exception as e:
        error_msg = f"❌ Ошибка при принудительном сохранении сессии: {e}"
        logger_msg(error_msg)
        SendlerOneCreate('').save_text(error_msg)

        # Пытаемся восстановить состояние браузера
        try:
            # Если есть несколько вкладок, закрываем лишние
            if len(driver.window_handles) > 1:
                current_handle = driver.current_window_handle
                for handle in driver.window_handles:
                    if handle != current_handle:
                        driver.switch_to.window(handle)
                        driver.close()
                driver.switch_to.window(current_handle)

            # Открываем нужный URL
            if saved_url:
                driver.get(saved_url)

        except Exception as recovery_error:
            logger_msg(f"❌ Ошибка при восстановлении состояния браузера: {recovery_error}")

        return False


def safe_force_save_session(driver, original_url: str) -> bool:
    """
    Безопасная обертка для принудительного сохранения сессии.
    Включает дополнительные проверки и обработку ошибок.
    
    Args:
        driver: WebDriver instance
        original_url (str): URL который нужно восстановить
        
    Returns:
        bool: True если операция прошла успешно, False в случае ошибки
    """
    if not driver:
        logger_msg("❌ Driver не инициализирован")
        return False

    if not original_url:
        logger_msg("❌ Не указан URL для восстановления")
        return False

    try:
        # Проверяем, что браузер отвечает
        driver.current_url
        return force_save_session(driver, original_url)

    except Exception as e:
        error_msg = f"❌ Критическая ошибка при работе с браузером: {e}"
        logger_msg(error_msg)
        SendlerOneCreate('').save_text(error_msg)
        return False
