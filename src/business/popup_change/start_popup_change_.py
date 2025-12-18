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
from src.utils.telegram_debug import SendlerOneCreate


def _exist_popup_change_promo(driver):
    try:
        driver.find_element(by=By.XPATH, value=f"//*[contains(*, 'акции изменились')] "
                                               f"| //*[contains(text(), 'акции изменились')]")
    except:
        return False

    return True


def _click_ignore_changes(driver):
    try:
        driver.find_element(by=By.XPATH, value=f"//*[contains(*, 'Продолжить работу')]/parent::button").click()
    except:
        return False

    return True


async def start_popup_change(settings):
    driver = settings['driver']

    for _try in range(3):
        is_exists_popup = _exist_popup_change_promo(driver)

        if not is_exists_popup:
            return False

        res_click = _click_ignore_changes(driver)

        await asyncio.sleep(1)

        continue

    error_ = 'Не смог нажать кнопку Продолжить в всплывающем окне "Акции изменились"'

    logger_msg(error_)

    SendlerOneCreate('').save_text(error_)

    return False
