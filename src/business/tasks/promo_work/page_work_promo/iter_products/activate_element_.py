# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from selenium.webdriver import ActionChains

from src.utils._logger import logger_msg


def activate_element(driver, element):
    try:
        ActionChains(driver).move_to_element(element).perform()
    except:
        error_ = f'Не смогу навестить на элемент'

        logger_msg(error_)

        return False

    return True
