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
import json

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

    promo_name = settings.get('promo_name', '')
    promo_time_sec = settings.get('promo_time_sec', None)
    promo_changes_count = settings.get('promo_changes_count', None)

    def _fmt_duration(sec):
        try:
            sec = float(sec)
        except Exception:
            return ''
        m, s = divmod(int(round(sec)), 60)
        h, m = divmod(m, 60)
        return f'{h:02d}:{m:02d}:{s:02d}'

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
        'Скидка, %',
        'Действие было',
        'Какое действие',
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

    total_products_count = 0

    # Простейшая мапа для перевода action на русский (расширяется при необходимости)
    action_map = {
        'enable': 'включение',
        'disable': 'выключение',
        'increase_price': 'повышение цены',
        'decrease_price': 'снижение цены',
        'apply_percent': 'применение скидки',
        'remove_percent': 'снятие скидки'
    }

    def to_state(select_val):
        return '✅' if bool(select_val) else '❌'

    def to_action_fields(action_val):
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
                percent,
                action_was,
                action_rus,
                price_salle,
                old_price,
                catalog_price,
            ])
            total_products_count += 1

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

    # Отправляем отчёт админам и менеджерам (менеджеры из БД settings)
    try:
        caption_lines = []
        caption_lines.append('📊 <b>Отчёт по акциям</b>')
        caption_lines.append(f'🏢 Кабинет: <code>{cabinet}</code>')
        if promo_name:
            caption_lines.append(f'🎯 Акция: <b>{promo_name}</b>')
        caption_lines.append(f'🗓️ Дата: <code>{ts}</code>')
        if promo_time_sec is not None:
            caption_lines.append(f'⏱️ Обработка: <code>{_fmt_duration(promo_time_sec)}</code>')
        caption_lines.append(f'📦 Товаров: <b>{total_products_count}</b>')
        if promo_changes_count is not None:
            try:
                caption_lines.append(f'🛠️ Изменений: <b>{int(promo_changes_count)}</b>')
            except Exception:
                caption_lines.append(f'🛠️ Изменений: <b>{promo_changes_count}</b>')
        caption = '\n'.join(caption_lines)
        sender = SendlerOneCreate(None)

        recipients = []
        for admin_id in ADMINS_REPORT or []:
            try:
                recipients.append(str(admin_id).strip())
            except Exception:
                pass

        async def _get_managers_from_db():
            ids = []
            BotDB = settings.get('BotDB')
            if not BotDB:
                return ids
            possible_keys = ['MANAGERS_REPORT', 'managers_report', 'REPORT_MANAGERS', 'MANAGERS']
            for key in possible_keys:
                try:
                    raw = await BotDB.settings.get_setting(key)
                except Exception:
                    raw = False
                if not raw:
                    continue
                data = None
                try:
                    data = json.loads(raw)
                except Exception:
                    data = raw
                try:
                    if isinstance(data, dict):
                        for k, v in data.items():
                            if isinstance(v, dict):
                                cid = str(v.get('chat_id', '')).strip()
                            else:
                                cid = str(v).strip()
                            if cid:
                                ids.append(cid)
                    elif isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict):
                                cid = str(item.get('chat_id', '')).strip()
                            else:
                                cid = str(item).strip()
                            if cid:
                                ids.append(cid)
                    elif isinstance(data, str):
                        for part in data.split(','):
                            cid = str(part).strip()
                            if cid:
                                ids.append(cid)
                except Exception:
                    pass
                if ids:
                    break
            unique = []
            seen = set()
            for cid in ids:
                if not cid:
                    continue
                if cid not in seen:
                    seen.add(cid)
                    unique.append(cid)
            return unique

        try:
            managers_ids = await _get_managers_from_db()
        except Exception:
            managers_ids = []

        for mid in managers_ids:
            recipients.append(str(mid).strip())

        for chat_id in recipients:
            if not chat_id:
                continue
            sender.send_file_to_id(excel_path, chat_id, caption)
    except Exception as es:
        from src.utils._logger import logger_msg
        logger_msg(f'Ошибка отправки Excel в телеграм: {es}')

    return excel_path
