# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import json

from settings import CHROME_PROFILE, PATCH_PROFILES
from src.browser.get_browser_and_close_ import get_browser_and_close
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate


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

        data_account = await self.BotDB.accounts.read_by_id(task.account_id)

        other_params = json.loads(task.parameters)

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
            await StartCheckAuth(self.settings).start_work()

            print()
