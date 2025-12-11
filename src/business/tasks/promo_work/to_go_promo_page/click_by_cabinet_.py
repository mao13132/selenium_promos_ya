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
from src.business.tasks.promo_work.load_more.load_more_ import load_more
from src.business.tasks.promo_work.to_go_promo_page.wait_load_cabinet_ import wait_load_cabinet


async def _click_by_cabinet(driver, cabinet):
    letters_up = "ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    letters_down = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя"

    try:

        driver.find_element(
            by=By.XPATH,
            value=(
                f"//*[contains(translate(text(), '{letters_up}', '{letters_down}'), "
                f"translate('{cabinet}', '{letters_up}', '{letters_down}'))]"
                f"/ancestor::*[contains(@data-e2e, 'business-card')]"
                f"//*[contains(text(), 'В кабинет')]"
            )
        ).click()
    except:
        return False

    return True


async def click_by_cabinet(settings):
    driver = settings['driver']

    cabinet_id = settings['cabinet_id']

    for _try in range(3):
        res_click = await _click_by_cabinet(driver, cabinet_id)

        if not res_click:
            await asyncio.sleep(1)

            res_ = await load_more({'driver': driver})

            continue

        full_load(driver)

        is_success = wait_load_cabinet(driver, '//*[contains(text(), "Динамика показов")]')

        if not is_success:
            await asyncio.sleep(1)

            continue

        return is_success

    error_ = f'Кончились попытки зайти на страницу кабинета'

    raise Exception(error_)
