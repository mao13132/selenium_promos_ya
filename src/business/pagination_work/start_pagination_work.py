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

from settings import WAIT_PRODUCT_TABLE_XPATH
from src.business.tasks.promo_work.to_go_promo_page.wait_load_cabinet_ import wait_load_cabinet
from src.utils._logger import logger_msg


def _click_next_btn(driver):
    try:
        driver.find_element(by=By.XPATH, value=f"//button[contains(@icon, 'ight')]").click()
    except:
        return False

    return True


async def next_page_btn(settings):
    driver = settings['driver']

    for _try in range(5):
        res_click = _click_next_btn(driver)

        # Если не кликается, то значит кнопки нет
        if not res_click:
            return False

        await asyncio.sleep(2)

        good_load = wait_load_cabinet(driver, WAIT_PRODUCT_TABLE_XPATH, count=120)

        if not good_load:
            await asyncio.sleep(1)

            continue

        return True

    error_ = f'Закончились попытки переключить страницу'

    logger_msg(error_)

    return False
