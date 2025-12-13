# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.tasks.promo_work.get_current_promos.start_get_current_promos import StartGetCurrentPromos
from src.business.tasks.promo_work.to_go_promo_page.start_to_go_promo_page_ import to_go_promo_page


class StartPromoLogic:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings['driver']
        self.task = settings['task']
        self.id_client = settings['id_client']
        self.cabinet = settings['cabinet']

    async def start_logic(self):
        print(f'Захожу в Yandex Partner в кабинет "{self.cabinet}" для работы')

        is_valid_cabinet = await to_go_promo_page(self.settings)

        if not is_valid_cabinet:
            error_ = f'Не смог зайти на страницу акций в кабинете "{self.cabinet}"'

            raise Exception(error_)

        await StartGetCurrentPromos(self.settings).start_work()

        return True
