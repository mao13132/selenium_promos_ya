# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time
from contextlib import contextmanager

from settings import NO_CREATE_BROWSER
from src.browser.create_browser_profile_ import create_browser_profile
from src.browser.graceful_browser_shutdown import graceful_browser_shutdown, emergency_browser_cleanup, \
    GracefulBrowserShutdown
from src.utils._logger import logger_msg


@contextmanager
def get_browser_and_close(path_chrome, name_profile_chrome, path_short_chrome):
    """Генератор браузера с автоматическим закрытием"""
    if NO_CREATE_BROWSER:
        yield False

        return False

    browser = None
    try:
        browser = create_browser_profile(path_chrome, name_profile_chrome, path_short_chrome)

        GracefulBrowserShutdown(browser.driver, name_profile_chrome)._close_extra_tabs()

        time.sleep(10)

        yield browser
    finally:
        if browser and hasattr(browser, 'driver') and browser.driver:
            try:
                # Сначала пробуем закрыть через CDP
                try:
                    setattr(browser.driver, '_closed_by_cdp', True)
                except Exception:
                    pass
                try:
                    browser.driver.execute_cdp_cmd("Browser.close", {})
                    print("Успешно закрыл браузер")
                except Exception:
                    pass

                # Если браузер уже закрыт через CDP, пропускаем любую попытку закрытия
                if getattr(browser.driver, '_closed_by_cdp', False):
                    pass
                else:
                    success = graceful_browser_shutdown(browser.driver, name_profile_chrome, timeout=30)

                    if success:
                        pass
                    else:
                        logger_msg("Грамотное закрытие не удалось, выполняю экстренную очистку")
                        emergency_browser_cleanup(browser.driver, name_profile_chrome)

                return True

            except Exception as cleanup_error:
                logger_msg(f"Ошибка при закрытии браузера: {cleanup_error}")

                # Последняя попытка экстренной очистки
                try:
                    # Не выполняем экстренную очистку, если закрыто через CDP
                    if not getattr(browser.driver, '_closed_by_cdp', False):
                        emergency_browser_cleanup(browser.driver, name_profile_chrome)
                except Exception as emergency_error:
                    logger_msg(f"Ошибка экстренной очистки: {emergency_error}")

                return False
