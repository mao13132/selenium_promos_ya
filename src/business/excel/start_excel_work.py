# ---------------------------------------------
# Program by @developer_telegrams
#
#
# Version   Date        Info
# 1.0       2023    Initial Version
#
# ---------------------------------------------
from datetime import datetime
import os

from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

from settings import ADMINS_REPORT
from src.utils.telegram_debug import SendlerOneCreate


async def start_excel_work(settings):
    """
    Генерирует Excel отчёт по товарам в разрезе: Кабинет → Акция → Товар
    и высылает файл администраторам из ADMINS_REPORT.

    Ожидаемый формат входных данных products_data:
    {
        0: {
            'name': {'name': 'Название акции'},
            'products': [
                {
                    'count_product': int,
                    'select': bool,              # участвует в акции
                    'name': str,                 # название товара
                    'stocks': int,               # остаток
                    'catalog_price': str,        # строка с ценой из каталога
                    'price_salle': str,          # цена по акции
                    'percent': int,              # процент скидки
                    'old_price': str,            # старая цена
                    'action': str                # тип действия (если было)
                }, ...
            ]
        }, ...
    }
    """
    products_data = settings.get('products_data', {}) or {}
    cabinet = settings.get('cabinet', '')

    # Подготовка пути для сохранения
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files_dir = os.path.join(base_dir, 'files')
    os.makedirs(files_dir, exist_ok=True)

    ts = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f"promos_{cabinet}_{ts}.xlsx".replace('/', '_').replace('\\', '_')
    excel_path = os.path.join(files_dir, filename)

    # Создаём книгу и лист
    wb = Workbook()
    ws = wb.active
    ws.title = 'Отчёт по акциям'

    # Заголовки
    headers = [
        'Кабинет',
        'Акция',
        'Товар',
        'Остаток',
        'Состояние',
        'Действие было',
        'Какое действие',
        'Скидка, %',
        'Цена по акции',
        'Старая цена',
        'Каталожная цена'
    ]
    ws.append(headers)

    # Стили заголовков
    bold = Font(bold=True)
    center = Alignment(horizontal='center', vertical='center', wrap_text=True)
    for col_idx in range(1, len(headers) + 1):
        cell = ws.cell(row=1, column=col_idx)
        cell.font = bold
        cell.alignment = center

    # Простейшая мапа для перевода action на русский (расширяется при необходимости)
    action_map = {
        'enable': 'включение',
        'disable': 'выключение',
        'increase_price': 'повышение цены',
        'decrease_price': 'снижение цены',
        'apply_percent': 'применение скидки',
        'remove_percent': 'снятие скидки'
    }

    def to_state(select_val: bool) -> str:
        return 'Галочка стоит' if bool(select_val) else 'Галочки нет'

    def to_action_fields(action_val: str) -> tuple[str, str]:
        if not action_val:
            return 'Нет', ''
        # Пытаемся перевести известный код действия на русский
        rus = action_map.get(str(action_val).strip(), str(action_val).strip())
        return 'Да', rus

    # Нормализуем iterable промо-данных
    items_iter = []
    if isinstance(products_data, dict):
        items_iter = list(products_data.values())
    elif isinstance(products_data, list):
        items_iter = products_data

    # Заполняем строки
    for promo_entry in items_iter:
        promo_name = ''
        try:
            promo_name = (promo_entry.get('name') or {}).get('name', '')
        except Exception:
            promo_name = str(promo_entry.get('name', ''))

        products = promo_entry.get('products', []) or []
        for product in products:
            name = product.get('name', '')
            stocks = product.get('stocks', '')
            select = product.get('select', False)
            action_val = product.get('action', '')
            percent = product.get('percent', '')
            price_salle = product.get('price_salle', '')
            old_price = product.get('old_price', '')
            catalog_price = product.get('catalog_price', '')

            state = to_state(select)
            action_was, action_rus = to_action_fields(action_val)

            ws.append([
                cabinet,
                promo_name,
                name,
                stocks,
                state,
                action_was,
                action_rus,
                percent,
                price_salle,
                old_price,
                catalog_price,
            ])

    # Автоширина столбцов по максимальной длине
    for col in ws.columns:
        max_len = 0
        col_letter = col[0].column_letter
        for cell in col:
            try:
                val = str(cell.value) if cell.value is not None else ''
                max_len = max(max_len, len(val))
            except Exception:
                pass
        ws.column_dimensions[col_letter].width = min(max_len + 2, 80)

    # Сохраняем файл
    wb.save(excel_path)

    # Отправляем отчёт всем администраторам
    try:
        caption = f'Отчёт по акциям: кабинет "{cabinet}" — {ts}'
        sender = SendlerOneCreate(None)
        for admin_id in ADMINS_REPORT:
            # поддержка числовых и строковых chat_id
            _id = str(admin_id)
            sender.send_file_to_id(excel_path, _id, caption)
    except Exception as es:
        # Логируем, но возвращаем путь к файлу, чтобы не терять результат
        from src.utils._logger import logger_msg
        logger_msg(f'Ошибка отправки Excel в телеграм: {es}')

    return excel_path
