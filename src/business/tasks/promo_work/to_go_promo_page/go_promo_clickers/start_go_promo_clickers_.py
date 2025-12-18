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

from src.business.full_load.full_load import full_load
from src.business.tasks.promo_work.to_go_promo_page.wait_load_cabinet_ import wait_load_cabinet
from src.utils._logger import logger_msg


def _click_promo_btn(driver):
    try:
        driver.find_element(by=By.XPATH,
                            value=f"//*[contains(@*[starts-with(name(), 'data-e2e')], 'promos') and "
                                  f"contains(text(), 'Акции')]").click()
    except:
        return False

    return True


def _click_promo_header(driver):
    try:
        driver.find_element(by=By.XPATH, value=f"//*[contains(@*[starts-with(name(), 'data-e2e')], 'promo')]").click()
    except:
        return False

    return True


async def start_go_promo_clickers(settings):
    driver = settings['driver']

    for _try in range(3):
        res_click = _click_promo_header(driver)

        is_open_popup = wait_load_cabinet(driver,
                                          f"//*[contains(@data-e2e, 'floating') and contains(@data-e2e, 'visible')]")

        if not is_open_popup:
            await asyncio.sleep(1)

            continue

        res_click_promo = _click_promo_btn(driver)

        full_load(driver)

        is_open_page = wait_load_cabinet(driver, f"//*[contains(@data-calendar-day, 'today')]", count=30)

        if not is_open_page:
            await asyncio.sleep(1)

            continue

        return True

    error_ = f'Закончились попытки зайти на страницу акций'

    logger_msg(error_)

    return False
