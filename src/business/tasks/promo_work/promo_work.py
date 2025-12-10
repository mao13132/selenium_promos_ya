# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json
from os import sep

from settings import CHROME_PROFILE, PATCH_PROFILES, MOKE_START_WORK, profiles_path
from src.browser.copy_profile_ import copy_profile
from src.browser.force_session_save_cdp import safe_force_save_session_cdp
from src.browser.get_browser_and_close_ import get_browser_and_close
from src.business.check_auth.start_check_auth import StartCheckAuth
from src.business.tasks.promo_work.start_promo_logic import StartPromoLogic
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate
from src.business.fake_task.fake_account_data import build_fake_account


class PromoWork:
    def __init__(self, settings, mode):
        self.settings = settings
        self.BotDB = settings['BotDB']
        self.mode = mode
        self.chrome_profile = CHROME_PROFILE
        self.path_chrome = f"{PATCH_PROFILES}{CHROME_PROFILE}"
        self.path_short_chrome = PATCH_PROFILES

    async def start_work(self, task):
        self.settings['mode'] = self.mode

        self.settings['task'] = task
        id_client = task.created_by_user_id
        self.settings['id_client'] = id_client

        if MOKE_START_WORK:
            data_account = build_fake_account(task.account_id)
        else:
            data_account = await self.BotDB.accounts.read_by_id(task.account_id)

        self.settings['data_account'] = data_account

        other_params = json.loads(task.parameters)

        cabinet = other_params.get('cabinet', False)

        cabinet_id = other_params.get('cabinet_id', False)

        percent_list = other_params.get('percent_list', '[]')

        self.settings['cabinet'] = cabinet

        self.settings['cabinet_id'] = cabinet_id

        self.settings['percent_list'] = json.loads(percent_list)

        with get_browser_and_close(self.path_chrome, self.chrome_profile, self.path_short_chrome) as browser:
            if not browser or not browser.driver:
                error_ = (f'❌ Задача с типом {task.task_type} (ID: {task.id_pk}) '
                          f'у аккаунта {data_account.name} (<code>ID: {data_account.id_pk}</code>) <b>завершилась с ошибкой</b>. '
                          f'Причина: не могу создать браузер')

                logger_msg(error_)
                await SendlerOneCreate('').send_msg_by_id(error_, id_client)
                raise Exception(error_)

            driver = browser.driver

            self.settings['driver'] = driver

            # Проверка авторизации
            check_auth = await StartCheckAuth(self.settings).start_work()

            if not check_auth:
                return False

            # Если получили 'is_user_auth', применяем принудительное сохранение сессии
            if str(check_auth) == 'is_user_auth':
                print("🔄 Применяем принудительное сохранение сессии перед перезапуском браузера")

                # Получаем текущий URL для восстановления после сохранения сессии
                current_url = driver.current_url

                # Выполняем принудительное сохранение сессии через CDP
                force_save_result = safe_force_save_session_cdp(driver, current_url)

                res_copy = await copy_profile({'path_chrome': self.path_chrome,
                                               'profile_path': f"{profiles_path}{sep}{self.chrome_profile}"})

            res_get_source = await StartPromoLogic(self.settings).start_logic()

            return True
