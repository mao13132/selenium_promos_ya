# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import time

from selenium.webdriver.common.by import By

from src.business.get_state_select.get_state_select_ import get_state_select


def _get_name(product):
    for _try in range(3):
        try:
            name = product.find_element(by=By.XPATH,
                                        value=f".//*[contains(@class, 'nameCategoryCol')]").text
        except:
            time.sleep(1)

            continue

        return name

    return ''


def _get_stocks(product):
    for _try in range(3):
        try:
            stocks = product.find_element(by=By.XPATH,
                                          value=f".//*[contains(@data-e2e, 'stock-total-count')] | "
                                                f".//*[contains(@*[starts-with(name(), 'data-e2e')], 'stock') and  "
                                                f"contains(@*[starts-with(name(), 'data-e2e')], 'empty')]").text
        except:
            time.sleep(1)

            continue

        if 'нет на складе' in str(stocks).lower():
            return 0

        try:
            stocks = int(stocks)
        except:
            time.sleep(1)

            continue

        return stocks

    return 0


def _get_price_by_catalog(product):
    for _try in range(3):
        try:
            price = product.find_element(by=By.XPATH,
                                         value=f".//*[contains(@data-zone-name, 'merchPrice')]").text
        except:
            time.sleep(1)

            continue

        return price

    return 0


def _get_price_salle(product):
    for _try in range(3):
        try:
            price = product.find_element(by=By.XPATH,
                                         value=f".//*[contains(@data-e2e, 'price-text')]//input").get_attribute('value')
        except:
            time.sleep(1)

            continue

        return price

    return 0


def _get_old_salle(product):
    for _try in range(3):
        try:
            old_price = product.find_element(by=By.XPATH,
                                         value=f".//*[contains(@data-e2e, 'old-price-text')]//input").get_attribute(
                'value')
        except:
            time.sleep(1)

            continue

        return old_price

    return 0


def _get_percent(product):
    for _try in range(3):
        try:
            percent = product.find_element(by=By.XPATH,
                                           value=f".//*[contains(@data-e2e, 'promo-discount')]").text
        except:
            time.sleep(1)

            continue

        try:
            percent_int = int(percent[:-1])
        except:
            return 0

        return percent_int

    return 0


async def extract_info_by_product(settings):
    count_product = settings['count_product']

    product = settings['product']

    select = get_state_select(product)

    name = _get_name(product)

    stocks = _get_stocks(product)

    catalog_price = _get_price_by_catalog(product)

    price_salle = _get_price_salle(product)

    percent = _get_percent(product)

    old_price = _get_old_salle(product)

    return_product_data = {
        'count_product': count_product,
        'select': select,
        'name': name,
        'stocks': stocks,
        'catalog_price': catalog_price,
        'price_salle': price_salle,
        'percent': percent,
        'old_price': old_price,
        'action': '',
    }

    return return_product_data
