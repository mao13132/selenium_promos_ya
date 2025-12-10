# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from selenium.webdriver.common.by import By

from src.utils._logger import logger_msg


def _get_all_rows(driver):
    try:
        rows = driver.find_elements(by=By.XPATH, value=f"//table/tbody//tr")
    except:
        return False

    return rows


async def get_all_products_rows(settings):
    driver = settings['driver']

    for _try in range(3):
        rows = _get_all_rows(driver)

        if not rows:
            await asyncio.sleep(1)

            continue

        return rows

    error_ = f'Закончились попытки получить строчки с товароми'

    logger_msg(error_)

    return False
