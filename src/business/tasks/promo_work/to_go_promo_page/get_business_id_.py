# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
import asyncio
from re import search

from selenium.webdriver.common.by import By


async def get_business_id(settings):
    driver = settings['driver']

    url_page = driver.current_url

    match = search(r"/business/(\d+)", url_page)

    if match:
        business_id = match.group(1)

        return business_id

    return False
