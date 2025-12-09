import time

from selenium.webdriver.common.by import By


class NewCaptcha:
    def __init__(self, driver):
        self.driver = driver

    def _check_url_capt(self):
        try:
            self._captcha_url = self.driver.current_url
        except Exception as es:
            print(f"Ошибка при заборе адресной строки. Капча '{es}'")
            return False

        if 'captcha' in self._captcha_url:
            return True

        return False

    def click_captcha(self):
        try:
            self.driver.find_element(by=By.XPATH,
                                     value=f"//form[@method='POST']"
                                           f"//*[contains(@class, 'CheckboxCaptcha-Anchor')]").click()
        except:
            return False

        return True

    def check_captcha(self):

        res_check = self._check_url_capt()

        if res_check:

            for _try in range(4):

                if _try > 0:
                    res_check = self._check_url_capt()

                    if not res_check:
                        return True

                print(f'Обнаружена капча')

                self.click_captcha()

                time.sleep(4)

            return True

        return False
