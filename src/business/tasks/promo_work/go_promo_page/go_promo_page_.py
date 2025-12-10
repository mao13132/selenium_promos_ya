# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from src.business.load_page.load_page import LoadPage


async def go_promo_page(settings):
    driver = settings['driver']

    url = settings['url']

    res_load = LoadPage(driver, url).loop_load_page(f"//*[contains(@data-calendar-day, 'today')]")

    return res_load
