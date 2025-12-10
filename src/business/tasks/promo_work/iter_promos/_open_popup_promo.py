# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By

from src.utils._logger import logger_msg


def _click_promo(promo):
    try:
        promo.click()
    except:
        return False

    return True


def _close_popup(driver):
    try:
        driver.find_element(by=By.XPATH, value=f"//*[contains(@class, 'header-close')]").click()
    except:
        return False

    return True


def _wait_open_popup(driver, _xpatch, count=1):
    try:
        WebDriverWait(driver, count).until(EC.presence_of_element_located((By.XPATH, _xpatch)))
    except:
        return False

    return True


async def open_popup_promo(settings):
    driver = settings['driver']

    promo = settings['promo']

    for _try in range(3):
        is_open = _wait_open_popup(driver, f"//a[contains(@*[starts-with(name(), 'data-e2e')], 'promo') and "
                                           f"contains(@*[starts-with(name(), 'data-e2e')], 'button')]", count=1)

        if is_open:
            res_close = _close_popup(driver)

            await asyncio.sleep(1)

            continue

        res_click = _click_promo(promo)

        if not res_click:
            await asyncio.sleep(1)

            continue

        is_open = _wait_open_popup(driver, f"//a[contains(@*[starts-with(name(), 'data-e2e')], 'promo') and "
                                           f"contains(@*[starts-with(name(), 'data-e2e')], 'button')]", count=5)

        if not is_open:
            await asyncio.sleep(1)

            continue

        return is_open

    error_ = f'Не смог открыть окно с акцией'

    logger_msg(error_)

    return False
