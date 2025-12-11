# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.business.tasks.promo_work.get_active_promos.get_active_promos_ import get_active_promos
from src.business.tasks.promo_work.go_promo_page.go_promo_page_ import go_promo_page
from src.business.tasks.promo_work.iter_promos._go_promos_page import go_promos_page
from src.business.tasks.promo_work.page_work_promo.start_page_work_promo import StartPageWorkPromo
from src.utils._logger import logger_msg
from src.utils.utils_decorators import catch_and_report


class IterPromos:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings['driver']
        self.task = settings['task']
        self.data_account = settings['data_account']
        self.id_client = settings['id_client']
        self.promos = settings['promos']
        self.data_promo = settings['data_promo']
        self.cabinet = settings['cabinet']

    @catch_and_report('⭕️ iter_promos')
    async def start_work(self):
        promo_url = self.driver.current_url

        full_products_all_promos = {}

        for count_promo, promo in enumerate(self.promos):
            name_promo = self.data_promo.get(count_promo, '')

            print(f'Начинаю заходить в акцию {name_promo}')

            # Если не в первый раз, то перезаходим на главную
            if count_promo > 0:
                is_to_go_page = await go_promo_page({'driver': self.driver, 'url': promo_url})

                if not is_to_go_page:
                    error_ = f'Не смог зайти на главную страницу акций "{self.cabinet}"'

                    logger_msg(error_)

                    continue

                await asyncio.sleep(3)

            promos = await get_active_promos({'driver': self.driver})

            try:
                promo = promos[count_promo]
            except:
                error_ = f'Не смог вытащить акцию с индексом {count_promo}'

                logger_msg(error_)

                continue

            is_good_load = await go_promos_page(
                {'driver': self.driver,
                 'promo': promo,
                 'cabinet': self.cabinet,
                 'name_promo': name_promo})

            if not is_good_load:
                continue

            product_history_from_promo = await StartPageWorkPromo(self.settings).start_work()

            full_products_all_promos[count_promo] = {
                'name': name_promo,
                'products': product_history_from_promo
            }

            continue

        return full_products_all_promos
