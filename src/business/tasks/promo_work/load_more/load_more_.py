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


def _click_load_more(driver):
    try:
        driver.find_element(by=By.XPATH,
                            value=f"//*[contains(@data-e2e, 'load') and contains(@data-e2e, 'next') and "
                                  f"contains(@data-e2e, 'button')]").click()
    except:
        return False

    return True


async def load_more(settings):
    driver = settings['driver']

    for _try in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        res_click = _click_load_more(driver)

        # Если нет кнопки выходит, успех
        if not res_click:
            return True

        await asyncio.sleep(3)

        continue

    error_ = f'Не смог нажать на кнопку загрузить ещё кабинеты'

    logger_msg(error_)

    return False
