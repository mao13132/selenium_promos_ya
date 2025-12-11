# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
class StartPagination:
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

    async def start_work(self):
        print()
