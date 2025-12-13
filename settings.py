import getpass
import os

from dotenv import load_dotenv
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


project_path = os.path.dirname(__file__)

profiles_path = os.path.join(os.path.dirname(__file__), 'profiles')

PATCH_PROFILES = f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data\\'

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

ADMIN = 1422194909

ADMINS_REPORT = ['1422194909']

TOKEN = os.getenv('TOKEN')

SQL_URL = os.getenv('SQL_URL')

CHROME_PROFILE = f'ya_ruslan'

NAME_PRODUCT = f'Анализатор Yandex Акций'

SITE_WORK = 'https://partner.market.yandex.ru/main-redirect'

WAIT_PRODUCT_TABLE_XPATH = f"//span[contains(text(), 'Цена по')]"

# Не создавать браузер
NO_CREATE_BROWSER = False

# Не менять состояние задач
MOKE_EDIT_TASK = False

# Не ожидать, а запускать задачу по promo
MOKE_START_WORK = False

TIME_KEY_SCHEDULE = 'schedule_minutes'
