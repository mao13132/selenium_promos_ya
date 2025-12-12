# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from src.business.pagination_work.start_pagination_work import next_page_btn
from src.business.save_changes.start_save_changes import save_changes
from src.business.tasks.promo_work.page_work_promo.end_scroll_page.end_scroll_page_ import is_end_scroll_page
from src.business.tasks.promo_work.page_work_promo.get_all_products_rows.get_all_products_rows_ import \
    get_all_products_rows
from src.business.iter_products.iter_products_ import IterProducts


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
        all_product_history = []

        count_page = 1

        count_scroll = 0

        print(f'Пролистываю страницу с товарами для их подгрузки')

        while True:
            is_end_page = is_end_scroll_page(self.driver)

            # Листаю в самый низ, пока не долистаю в самый низ
            if not is_end_page:
                self.driver.execute_script("window.scrollBy(0, 200);")

                await asyncio.sleep(1)

                count_scroll += 1

                continue

            # В самом низу страницы
            await asyncio.sleep(3)

            all_rows = await get_all_products_rows(self.settings)

            work_from_products = await IterProducts(self.settings).start_work(all_rows)

            products_history = work_from_products.get('products_history', [])

            all_product_history.extend(products_history)

            is_change = work_from_products.get('is_change', False)

            if is_change:
                res_ = await save_changes(self.settings)

            print(f'Конец страницы {count_page}')

            next_page = await next_page_btn(self.settings)

            if not next_page:
                print(f'Работа по акции закончена. Все страницы обработаны')

                return all_product_history

            count_page += 1

            continue

        return all_product_history


