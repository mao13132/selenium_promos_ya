# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time

from selenium.webdriver.common.by import By


def get_state_select(product):
    for _try in range(3):
        try:
            status = product.find_element(by=By.XPATH, value=f".//td//input[@type='checkbox']").get_attribute('checked')
        except:
            time.sleep(1)

            continue

        if 'true' in str(status):
            return True
        else:
            return False

    return False
