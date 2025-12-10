# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.tasks.promo_work.page_work_promo.extract_info_by_product.extract_info_by_product_ import \
    extract_info_by_product
from src.business.tasks.promo_work.page_work_promo.iter_products.activate_element_ import activate_element


class IterProducts:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings['driver']
        self.task = settings['task']
        self.data_account = settings['data_account']
        self.id_client = settings['id_client']
        self.promos = settings['promos']
        self.data_promo = settings['data_promo']
        self.cabinet = settings['cabinet']

    async def start_work(self, products):
        is_change = False

        for product in products:
            activate_element(self.driver, product)

            data_product = await extract_info_by_product({'driver': self.driver, 'product': product})

            print()
