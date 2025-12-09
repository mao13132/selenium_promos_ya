# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
import logging

from src.business.start_work import StartWork

from src.business.start_business import StartBusiness
from src.utils._logger import logger_msg
from src.utils.telegram_debug import SendlerOneCreate
from src.utils.utils_decorators import catch_and_report
from src.sql.connector import BotDB

import warnings

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

logging.basicConfig(handlers=[logging.FileHandler(filename="./logs.txt",
                                                  encoding='utf-8', mode='a+')],
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
                    datefmt="%F %A %T",
                    level=logging.ERROR)


@catch_and_report('⭕️ Ошибка главного потока')
async def main():
    res_init = await BotDB.init_bases()

    if not res_init:
        msg = f'WB Lock: Нет подключения к базе данных. Останавливаю работу'

        SendlerOneCreate('').save_text(msg)

        logger_msg(msg)

        return 'no_sql'

    settings = {
        'BotDB': BotDB,
    }

    res_ = await StartBusiness(settings).start_business()

    return res_


if __name__ == '__main__':
    asyncio.run(main())
    print(f'Бот остановлен')
