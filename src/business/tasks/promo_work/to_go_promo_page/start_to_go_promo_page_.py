# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from settings import SITE_WORK
from src.business.load_page.load_page import LoadPage
from src.business.tasks.promo_work.to_go_promo_page.click_by_cabinet_ import click_by_cabinet


async def to_go_promo_page(settings):
    driver = settings['driver']

    cabinet_id = settings['cabinet_id']

    res_load = LoadPage(driver, SITE_WORK).loop_load_page(f"//*[contains(*, 'Все кабинеты')] | "
                                                          f"//*[contains(text(), 'Все кабинеты')]")

    if not res_load:
        return False

    res_to_go_cabinet = await click_by_cabinet(settings)

    if not res_to_go_cabinet:
        return False

    print()
