import getpass
import os

from dotenv import load_dotenv

project_path = os.path.dirname(__file__)

profiles_path = os.path.join(os.path.dirname(__file__), 'profiles')

PATCH_PROFILES = f'C:\\Users\\{getpass.getuser()}\\AppData\\Local\\Google\\Chrome\\User Data\\'

dotenv_path = os.path.join(os.path.dirname(__file__), 'src', '.env')

load_dotenv(dotenv_path)

ADMIN = 1422194909

TOKEN = os.getenv('TOKEN')

CHROME_PROFILE = f'79054738463'

NAME_PRODUCT = f'Анализатор Yandex Акций'

SITE_WB_SERVICE = 'https://service.wb.ru/'
