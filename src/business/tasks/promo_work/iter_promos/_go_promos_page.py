# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from settings import WAIT_PRODUCT_TABLE_XPATH
from src.business.tasks.promo_work.iter_promos._open_popup_promo import open_popup_promo

from selenium.webdriver.common.by import By

from src.business.tasks.promo_work.to_go_promo_page.wait_load_cabinet_ import wait_load_cabinet
from src.utils._logger import logger_msg


def _click_go_promo_btn(driver):
    try:
        driver.find_element(by=By.XPATH,
                            value=f"//*[contains(@*[starts-with(name(), 'data-e2e')], 'bestseller') and "
                                  f"contains(@*[starts-with(name(), 'data-e2e')], 'details')]").click()
    except:
        return False

    return True


async def go_promos_page(settings):
    driver = settings['driver']

    is_open = await open_popup_promo(settings)

    if not is_open:
        return False

    for _try in range(3):
        res_click_promo = _click_go_promo_btn(driver)

        if not res_click_promo:
            await asyncio.sleep(1)

            continue

        good_load = wait_load_cabinet(driver, WAIT_PRODUCT_TABLE_XPATH, count=120)

        if not good_load:
            await asyncio.sleep(1)

            continue

        return True

    error_ = f'Не смог зайти в акцию'

    logger_msg(error_)

    return False
