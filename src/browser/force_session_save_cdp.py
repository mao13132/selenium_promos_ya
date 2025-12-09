# ---------------------------------------------
# Program by @developer_telegrams
# Force Session Save Module (CDP)
#
# Версия CDP: принудительное сохранение сессии и закрытие браузера
# через Chrome DevTools Protocol
# ---------------------------------------------

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def force_save_session_cdp(driver, original_url: str, close_browser: bool = True) -> bool:
    """
    Принудительно сохраняет сессию браузера через переключение вкладок
    и корректно закрывает браузер через CDP.

    Алгоритм:
    1) Открыть новую вкладку с Google
    2) Дождаться загрузки
    3) Закрыть исходную вкладку
    4) Ожидать
    5) Открыть сохранённый URL в новой вкладке
    6) Дождаться полной загрузки
    7) Разрешить скачивания и закрыть браузер через CDP (опционально)

    Args:
        driver: WebDriver
        original_url: URL для восстановления
        close_browser: закрыть браузер через CDP после сохранения

    Returns:
        bool: статус операции
    """
    # Сохраняем URL для восстановления: либо переданный, либо текущий URL из драйвера
    saved_url = original_url or getattr(driver, "current_url", "")

    try:
        # Запоминаем handle исходной вкладки, чтобы позже её закрыть
        original_window = driver.current_window_handle

        # Открываем новую вкладку: это триггерит сохранение части данных профиля (cookies/storage)
        driver.switch_to.new_window("tab")

        # Загружаем «тяжёлую» страницу (Google), чтобы инициировать дисковую запись профиля
        driver.get("https://www.google.com")

        # Ждём появления поисковой строки — индикатор полной загрузки страницы
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "q")))

        # Ищем handle новой вкладки (любой, отличный от исходной)
        new_window = None
        for handle in driver.window_handles:
            if handle != original_window:
                new_window = handle
                break

        if not new_window:
            logger_msg("Не удалось найти новую вкладку")
            return False

        # Возвращаемся на исходную вкладку и закрываем её — это помогает зафиксировать сессию
        driver.switch_to.window(original_window)
        driver.close()

        # Переключаемся на оставшуюся вкладку (Google) и даём время системе
        driver.switch_to.window(new_window)
        time.sleep(5)

        # Открываем сохранённый URL в новой вкладке
        driver.switch_to.new_window("tab")
        driver.get(saved_url)

        # Дожидаемся полной готовности документа (readyState == complete)
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        # Небольшая пауза для завершения фоновых операций записи профиля
        time.sleep(5)

        if close_browser:
            # Разрешаем скачивания, чтобы закрытие не блокировалось политиками загрузок
            try:
                driver.execute_cdp_cmd("Page.setDownloadBehavior", {"behavior": "allow"})
            except Exception:
                pass

            # Помечаем драйвер как закрытый через CDP, чтобы контекст-менеджер не пытался закрывать повторно
            try:
                setattr(driver, "_closed_by_cdp", True)
            except Exception:
                pass

            # Закрываем весь браузер через протокол DevTools
            try:
                driver.execute_cdp_cmd("Browser.close", {})
            except Exception as close_err:
                logger_msg(f"Ошибка закрытия браузера через CDP: {close_err}")

        return True

    except Exception as e:
        # Логируем и отправляем уведомление при любой ошибке процесса сохранения
        error_msg = f"❌ Ошибка при принудительном сохранении сессии (CDP): {e}"
        logger_msg(error_msg)
        SendlerOneCreate("").save_text(error_msg)
        return False


def safe_force_save_session_cdp(driver, original_url: str) -> bool:
    """
    Безопасная обёртка с проверками для CDP-логики.
    """
    # Проверка валидности драйвера
    if not driver:
        logger_msg("❌ Driver не инициализирован")
        return False

    # Если URL не передан, пытаемся взять текущий из драйвера
    if not original_url:
        try:
            original_url = driver.current_url
        except Exception:
            logger_msg("❌ Не указан URL для восстановления")
            return False

    try:
        # Проверяем, что браузер отвечает, затем запускаем основную процедуру
        _ = driver.current_url
        return force_save_session_cdp(driver, original_url, close_browser=True)
    except Exception as e:
        # В случае критической ошибки аккуратно логируем и уведомляем
        error_msg = f"❌ Критическая ошибка при работе с браузером (CDP): {e}"
        logger_msg(error_msg)
        SendlerOneCreate("").save_text(error_msg)
        return False