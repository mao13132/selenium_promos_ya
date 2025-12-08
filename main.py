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
from src.utils.utils_decorators import catch_and_report

import warnings

warnings.filterwarnings("ignore", message="pkg_resources is deprecated")

logging.basicConfig(handlers=[logging.FileHandler(filename="./logs.txt",
                                                  encoding='utf-8', mode='a+')],
                    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
                    datefmt="%F %A %T",
                    level=logging.ERROR)


@catch_and_report('⭕️ Ошибка главного потока')
async def main():
    settings_work = {}

    res_work = await StartWork(settings_work).start_work()

    print(f'Работа завершена')

    return res_work


if __name__ == '__main__':
    asyncio.run(main())
    print(f'Бот остановлен')
