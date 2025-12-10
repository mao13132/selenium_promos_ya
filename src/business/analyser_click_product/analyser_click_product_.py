# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
async def analyser_click_product(settings):
    data_product = settings['data_product']

    percent_list = settings['percent_list']

    # Если процент подходящий и продукт не отмечен, то нужно включить
    if data_product['percent'] in percent_list and not data_product['select']:
        return {'action': 'enable'}

    # Если процент не подходящий, но товар отмечен, то нужно выключить
    if data_product['percent'] not in percent_list and data_product['select']:
        return {'action': 'disable'}

    # Если остаток 0, и товар отмечен, то нужно выключить
    if data_product['stocks'] == 0 and data_product['select']:
        return {'action': 'disable'}

    return False
