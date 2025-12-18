# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import time

from selenium.webdriver.common.by import By

from settings import WAIT_PRODUCT_TABLE_XPATH, COUNT_PRODUCT_FROM_PAGE
from src.business.tasks.promo_work.to_go_promo_page.wait_load_cabinet_ import wait_load_cabinet
from src.utils._logger import logger_msg


def _get_status_target_count(driver, target_count):
    try:
        class_name = driver.find_element(by=By.XPATH, value=f"//*[@title='{target_count}']").get_attribute('class')
    except:
        time.sleep(1)

        return False

    if 'disable' in str(class_name).lower():
        return True

    return False


def _click_target_count(driver, target_count):
    try:
        driver.find_element(by=By.XPATH, value=f"//*[@title='{target_count}']").click()
    except:
        return False

    return True


async def change_count_for_page(settings):
    driver = settings['driver']

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except Exception as es:
        error_ = f'change_count_for_page: Ошибка при работе на странице {es} '

        logger_msg(error_)

        try:
            driver.refresh()
        except:
            pass

    for _try in range(3):
        activate_target_count = _get_status_target_count(driver, COUNT_PRODUCT_FROM_PAGE)

        if activate_target_count:
            driver.execute_script("window.scrollTo(0, 0);")
            return True

        res_click = _click_target_count(driver, COUNT_PRODUCT_FROM_PAGE)

        good_load = wait_load_cabinet(driver, WAIT_PRODUCT_TABLE_XPATH, count=120)

        if not good_load:
            await asyncio.sleep(1)

            continue

        continue

    error_ = f'Не смог переключить на нужное кол-во товаров на странице'

    logger_msg(error_)

    return False
