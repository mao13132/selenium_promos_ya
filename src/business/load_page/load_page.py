import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from settings import NAME_PRODUCT
from src.business.captcha.new_captcha import NewCaptcha
from src.utils._logger import logger_msg


class LoadPage:
    def __init__(self, driver, url):
        self.url = url
        self.driver = driver
        self.source_name = NAME_PRODUCT

    def load_page(self, url):
        try:
            self.driver.get(url)
            return True
        except:
            return False

    def __check_load_page(self, _xpatch):
        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, _xpatch)))
            return True
        except:
            return False

    def loop_load_page(self, _xpatch):
        count = 0

        count_ower = 10

        self.driver.set_page_load_timeout(60)

        while True:

            count += 1

            if count >= count_ower:
                msg = f'Не смог открыть {self.source_name} проверьте прокси'

                logger_msg(msg)

                return False

            start_page = self.load_page(self.url)

            check_captcha = NewCaptcha(self.driver).check_captcha()

            if check_captcha:

                time.sleep(2)

                continue

            if not start_page:

                time.sleep(5)

                continue

            check_page = self.__check_load_page(_xpatch)

            if not check_page:
                self.driver.refresh()

                continue

            self.driver.set_page_load_timeout(60)

            return True
