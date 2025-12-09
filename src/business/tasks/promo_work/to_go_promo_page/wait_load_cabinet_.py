# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def wait_load_cabinet(driver, _xpatch, count=5):
    try:
        WebDriverWait(driver, count).until(
            EC.presence_of_element_located((By.XPATH, _xpatch)))
    except:
        return False

    return True
