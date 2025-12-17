# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.tasks.promo_work.extract_info_by_promo.extract_info_by_promo_ import extract_info_by_promo
from src.business.tasks.promo_work.get_active_promos.get_active_promos_ import get_active_promos
from src.business.tasks.promo_work.get_today_date.get_today_date_ import get_today_date
from src.business.iter_promos.iter_promos_ import IterPromos
from src.utils.utils_decorators import catch_and_report


class StartGetCurrentPromos:
    def __init__(self, settings):
        self.settings = settings
        self.driver = settings['driver']
        self.task = settings['task']
        self.id_client = settings['id_client']
        self.cabinet = settings['cabinet']

    @catch_and_report('StartGetCurrentPromos')
    async def start_work(self):
        date_today = await get_today_date({'driver': self.driver})

        if not date_today:
            return False

        # Получаю активные акции для получения их названий
        promos = await get_active_promos({'driver': self.driver})

        if not promos:
            return False

        self.settings['promos'] = promos

        data_promo = await extract_info_by_promo({'driver': self.driver, 'promos': promos})

        self.settings['data_promo'] = data_promo

        products_data = await IterPromos(self.settings).start_work()

        return products_data
