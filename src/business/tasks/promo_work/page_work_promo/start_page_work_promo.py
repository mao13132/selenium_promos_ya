# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.business.tasks.promo_work.page_work_promo.end_scroll_page.end_scroll_page_ import is_end_scroll_page
from src.business.tasks.promo_work.page_work_promo.get_all_products_rows.get_all_products_rows_ import \
    get_all_products_rows
from src.business.tasks.promo_work.page_work_promo.iter_products.iter_products_ import IterProducts


class StartPageWorkPromo:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings['driver']
        self.task = settings['task']
        self.data_account = settings['data_account']
        self.id_client = settings['id_client']
        self.promos = settings['promos']
        self.data_promo = settings['data_promo']
        self.cabinet = settings['cabinet']

    async def start_work(self):
        count_page = 1

        while True:
            is_end_page = is_end_scroll_page(self.driver)

            # Листаю в самый низ, пока не долистаю в самый низ
            if not is_end_page:
                self.driver.execute_script("window.scrollBy(0, 150);")

                await asyncio.sleep(1)

                continue

            # В самом низу страницы

            await asyncio.sleep(3)

            all_rows = await get_all_products_rows(self.settings)

            print(f'На {count_page} странице {len(all_rows)} товаров')

            work_from_products = await IterProducts(self.settings).start_work(all_rows)

            print(f'Конец страницы')

            print()

        print()


