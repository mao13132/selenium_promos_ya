# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import SITE_WORK
from src.business.load_page.load_page import LoadPage

from selenium.webdriver.common.by import By

from src.utils.telegram_debug import SendlerOneCreate


class StartCheckAuth:
    def __init__(self, settings):
        self.settings = settings

        self.driver = settings['driver']

        self.url = SITE_WORK

    async def check_is_auth(self):
        try:
            self.driver.find_element(
                by=By.XPATH,
                value=f"//*[contains(@class, 'wrapper_login')]//*[contains(text(), 'Войти') and "
                      f"contains(@class, 'login') and contains(@class, 'header')]")
        except:
            return True

        return False

    async def start_work(self):
        is_user_auth = False

        is_auth = False

        for _try in range(3):
            print(f'Захожу в Yandex Partner для проверки авторизации')

            res_load = LoadPage(self.driver, self.url).loop_load_page(f"//*[contains(*, 'Войти')] | "
                                                                      f"//*[contains(text(), 'Войти')] | "
                                                                      f"//*[contains(*, 'Все кабинеты')] | "
                                                                      f"//*[contains(text(), 'Все кабинеты')]")

            if not res_load:
                return False

            is_auth = await self.check_is_auth()

            if not is_auth:
                error_ = f'❌ Анализатор Yandex акции: Нет авторизации. Пожалуйста, пройдите авторизацию'

                SendlerOneCreate('').save_text(error_)

                input(f'Нет авторизации в браузере. Пройдите авторизацию и после нажмите ЗДЕСЬ любую кнопку')

                is_user_auth = True

                continue
            else:
                is_auth = True

                break

        # Если пользователь проходил авторизацию
        if is_user_auth:
            return 'is_user_auth'

        return is_auth
