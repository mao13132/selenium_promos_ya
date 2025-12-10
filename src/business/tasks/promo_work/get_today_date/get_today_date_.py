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


def _get_today_date(driver):
    try:
        today = driver.find_element(by=By.XPATH, value=f"//*[contains(@data-calendar-day, 'today')]").text
    except:
        return False

    return today


async def get_today_date(settings):
    driver = settings['driver']

    for _try in range(3):
        day = _get_today_date(driver)

        if not day:
            await asyncio.sleep(1)

            continue

        return day

    error_ = f'Не смог получить текущую дату'

    raise Exception(error_)
