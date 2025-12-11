import requests

from settings import TOKEN, ADMIN
from src.utils._logger import logger_msg


class SendlerOneCreate:
    def __init__(self, driver):
        self.TOKEN = TOKEN

        self.ADMIN_TELEGRAM = ADMIN

        self.driver = driver

    def save_text(self, text):
        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendMessage" + "?chat_id=" + \
                  str(self.ADMIN_TELEGRAM) + "&text=" + text

        try:
            results = requests.get(url_req)
        except Exception as es:
            msg = f'Ошибка при отправке сообщения в телеграм "{es}"'

            logger_msg(msg)

            return False

        return True

    def send_msg_by_id(self, text, id_user):
        # Формируем данные для отправки
        data = {
            "chat_id": id_user,
            "text": text,
            "parse_mode": "HTML",
        }

        url_req = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"

        try:
            response = requests.post(url_req, json=data)
            response.raise_for_status()
        except Exception as es:
            msg = f'Ошибка при отправке сообщения с клавиатурой в телеграм "{es}"'
            logger_msg(msg)
            return False

        return True

    def send_file(self, file, text_):
        file_in = open(file, 'rb')

        open_files = {'document': file_in}

        cap = {'caption': text_}

        url_req = "https://api.telegram.org/bot" + self.TOKEN + "/sendDocument?chat_id=" + str(self.ADMIN_TELEGRAM)

        try:
            response = requests.post(url_req, files=open_files, data=cap)

        except Exception as es:
            msg = f'Ошибка при отправке сообщения с файлом в телеграм "{es}"'

            logger_msg(msg)

            return False

        file_in.close()

        print(f"Отправил файл в телеграм")

        return True

    def send_file_to_id(self, file, id_user, text_):
        file_in = open(file, 'rb')

        open_files = {'document': file_in}
        data = {'chat_id': id_user, 'caption': text_}

        url_req = f"https://api.telegram.org/bot{self.TOKEN}/sendDocument"

        try:
            response = requests.post(url_req, files=open_files, data=data)
            response.raise_for_status()
        except Exception as es:
            msg = f'Ошибка при отправке файла в телеграм пользователю {id_user} "{es}"'
            logger_msg(msg)
            file_in.close()
            return False

        file_in.close()
        print(f"Отправил файл пользователю {id_user} в телеграм")
        return True

    async def send_msg_with_keyboard(self, text, id_user, task_id):
        """
        Отправляет сообщение с inline клавиатурой для ввода SMS кода
        
        Args:
            text (str): Текст сообщения
            id_user (str): ID пользователя (токен бота)
            task_id (str): ID задачи для callback
        
        Returns:
            bool: True если успешно, False если ошибка
        """
        # Создаем inline клавиатуру
        keyboard = {
            "inline_keyboard": [[
                {
                    "text": "Ввести SMS код",
                    "callback_data": f"get_sms-{task_id}"
                }
            ]]
        }

        # Формируем данные для отправки
        data = {
            "chat_id": id_user,
            "text": text,
            "parse_mode": "HTML",
            "reply_markup": keyboard
        }

        url_req = f"https://api.telegram.org/bot{self.TOKEN}/sendMessage"

        try:
            response = requests.post(url_req, json=data)
            response.raise_for_status()
        except Exception as es:
            msg = f'Ошибка при отправке сообщения с клавиатурой в телеграм "{es}"'
            logger_msg(msg)
            return False

        return True
