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


def _get_active_promos(driver):
    try:
        promos = driver.find_elements(by=By.XPATH, value=f"//*[contains(@calendar-item-status, 'active-calendar-item')]")
    except:
        return False

    return promos


async def get_active_promos(settings):
    driver = settings['driver']

    for _try in range(3):
        promos = _get_active_promos(driver)

        if not promos or len(promos) < 1:
            await asyncio.sleep(1)

            continue

        return promos

    error_ = f'Не могу получить активные акции'

    raise Exception(error_)
