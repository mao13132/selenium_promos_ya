# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time

from selenium.webdriver.common.by import By

from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def is_big_loading_spinner(driver):
    try:
        spinner = driver.find_element(by=By.XPATH, value=f"//div[contains(@class, 'general-preloader')]")
    except:
        return False

    try:
        before_content = driver.execute_script(
            'return window.getComputedStyle(arguments[0], "::before").getPropertyValue("content");',
            spinner
        )
    except:
        return False

    if not before_content:
        return False

    if str(before_content) == '""':
        return False

    return True


def full_load(driver):
    for _try in range(60):
        try:
            status = driver.execute_script("return document.readyState")
        except Exception as es:
            error = f'Не могу получить статус загрузки страницы "{es}"'

            logger_msg(error)

            SendlerOneCreate('').save_text(error)

            return False

        time.sleep(1)

        if status == 'complete':
            return True

        time.sleep(1)

        continue


def full_load_big_spinner(driver):
    for _try in range(60):
        try:
            status = driver.execute_script("return document.readyState")
        except Exception as es:
            error = f'Не могу получить статус загрузки страницы "{es}"'

            logger_msg(error)

            SendlerOneCreate('').save_text(error)

            return False

        time.sleep(1)

        is_loader = is_big_loading_spinner(driver)

        if status == 'complete' and not is_loader:
            return True

        time.sleep(1)

        continue
