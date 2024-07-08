import csv
import json
import logging
import os
from typing import Any, Dict, List

import openpyxl

# Создаем и настраиваем логгер
log_file = os.path.join(os.path.dirname(__file__), '..', 'logs', 'utils.log')
os.makedirs(os.path.dirname(log_file), exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)s %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('utils')


def read_transactions_from_json(json_file_path: str) -> List[Dict[str, Any]]:
    """
    Читает транзакции из JSON-файла и возвращает их в виде списка словарей.

    Args:
        json_file_path (str): Путь к JSON-файлу.

    Returns:
        List[Dict[str, Any]]: Список транзакций, если файл корректный. Пустой список в случае ошибки.
    """
    logger.debug("Попытка чтения JSON-файла: %s", json_file_path)
    try:
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.debug("Успешно прочитан JSON-файл: %s", json_file_path)
                return data
            else:
                logger.error("Неверный формат данных в файле: %s", json_file_path)
                return []
    except FileNotFoundError:
        logger.error("Файл не найден: %s", json_file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Ошибка декодирования JSON в файле: %s", json_file_path)
        return []


def read_transactions_from_csv(file_name: str) -> List[Dict[str, str]]:
    transactions: List[Dict[str, str]] = []
    current_dir = os.path.dirname(__file__)  # Получаем текущий каталог скрипта
    file_path = os.path.join(current_dir, file_name)  # Формируем полный путь к файлу

    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        for row in reader:
            transactions.append(dict(row))

    return transactions


def read_transactions_from_xlsx(xlsx_file: str) -> List[Dict[str, str]]:
    transactions = []
    workbook = openpyxl.load_workbook(xlsx_file)
    sheet = workbook.active
    headers = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        transactions.append(dict(zip(headers, row)))

    return transactions

# В других частях вашего проекта, где вам нужно считать данные из CSV
# или XLSX файлов, вы можете импортировать эти функции следующим образом:
#
# from utils import read_transactions_from_csv, read_transactions_from_xlsx
#
# # Пример использования для CSV
# csv_file = '/home/alex/Загрузки/transactions.csv'
# csv_transactions = read_transactions_from_csv(csv_file)
# print(csv_transactions)
#
# # Пример использования для XLSX
# xlsx_file = '/home/alex/Загрузки/transactions_excel.xlsx'
# xlsx_transactions = read_transactions_from_xlsx(xlsx_file)
# print(xlsx_transactions)
