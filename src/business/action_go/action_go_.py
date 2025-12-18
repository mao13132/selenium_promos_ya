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

from src.business.get_state_select.get_state_select_ import get_state_select
from src.business.popup_change.start_popup_change_ import start_popup_change
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


def _click_selector(product):
    try:
        product.find_element(by=By.XPATH, value=f".//td//input[@type='checkbox']").click()
    except:
        return False

    return True


async def action_go(settings):
    driver = settings['driver']

    product = settings['product']

    action = settings['action']

    data_product = settings['data_product']

    for _try in range(4):
        if _try > 0:
            is_change_promo = await start_popup_change({"driver": driver})

        status_selector = get_state_select(product)

        # Включен
        if action == 'enable' and status_selector:
            return True

        # Выключен
        if action == 'disable' and not status_selector:
            return True

        res_click = _click_selector(product)

        await asyncio.sleep(1)

        continue

    error_ = f'Не смог обработать товар {str(data_product)} необходимо перевести задачу в {action}'

    logger_msg(error_)

    SendlerOneCreate('').save_text(error_)

    return False
