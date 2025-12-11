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

XPATH_SAVE_BTN = f"//*[contains(@*[starts-with(name(), 'data-e2e')], 'promo') and " \
                 f"contains(@*[starts-with(name(), 'data-e2e')], 'save')]"


def _exists_save_btn(driver):
    try:
        driver.find_element(by=By.XPATH, value=XPATH_SAVE_BTN)
    except:
        return False

    return True


def _click_save_btn(driver):
    try:
        driver.find_element(by=By.XPATH, value=XPATH_SAVE_BTN).click()
    except:
        return False

    return True


async def save_changes(settings):
    driver = settings['driver']

    for _try in range(3):
        exists = _exists_save_btn(driver)

        if not exists:
            return True

        res_click = _click_save_btn(driver)

        await asyncio.sleep(1)

        continue

    error_ = f'Не смог нажать на кнопку сохранить изменения'

    logger_msg(error_)

    return True
