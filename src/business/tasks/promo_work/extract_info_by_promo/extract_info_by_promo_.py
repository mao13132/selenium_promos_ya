# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio

from selenium.webdriver.common.by import By


def _get_name_promo(promo):
    try:
        name = promo.find_element(by=By.XPATH, value=f".//span[contains(@class, 'use')]").text
    except:
        return False

    return name


async def extract_info_by_promo(settings):
    promos = settings['promos']

    data_promos = {}

    for count, promo in enumerate(promos):
        for _try in range(3):
            name = _get_name_promo(promo)

            if not name:
                await asyncio.sleep(1)

                continue

            data_promos[count] = {'name': name}

            continue

        continue

    return data_promos
