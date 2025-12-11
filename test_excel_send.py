import argparse
import asyncio

from temp.products_data import products_data
from src.business.excel.start_excel_work import start_excel_work


def main():
    parser = argparse.ArgumentParser(
        description='Тест генерации Excel и отправки админам по ADMINS_REPORT'
    )
    parser.add_argument('--cabinet', default='Я.Store', help='Название кабинета')

    args = parser.parse_args()

    path = asyncio.run(start_excel_work({'products_data': products_data, 'cabinet': args.cabinet}))

    print(f'Готово. Файл: {path}')
    print('Если ADMINS_REPORT не пуст — файл отправлен админам.')


if __name__ == '__main__':
    main()
