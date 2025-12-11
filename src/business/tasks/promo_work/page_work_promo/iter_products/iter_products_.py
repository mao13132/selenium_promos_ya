# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.action_go.action_go_ import action_go
from src.business.analyser_click_product.analyser_click_product_ import analyser_click_product
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
        self.percent_list = settings['percent_list']

    async def start_work(self, products):
        products_history = []

        is_change = False

        for count_product, product in enumerate(products):
            activate_element(self.driver, product)

            self.driver.execute_script("window.scrollBy(0, 50);")

            data_product = await extract_info_by_product(
                {'driver': self.driver,
                 'product': product,
                 'count_product': count_product
                 })

            products_history.append(data_product)

            need_click = await analyser_click_product(
                {'data_product': data_product,
                 'percent_list': self.percent_list
                 })

            if not need_click:
                # print(f'\nТовар {data_product["name"]} не нуждается в действиях\n')

                continue

            # Распаковываю action
            action = need_click['action']

            data_product['action'] = action

            res_action_work = await action_go(
                {'driver': self.driver, 'product': product, 'action': action, 'data_product': data_product})

            if res_action_work:
                is_change = True

            print(f'\n{count_product} Изменил состояние для товара ({action}) {data_product["name"]}\n')

            continue

        return_dict = {
            'is_change': is_change,
            'products_history': products_history
        }

        return return_dict
