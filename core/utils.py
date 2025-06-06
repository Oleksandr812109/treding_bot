import logging
import configparser
from datetime import datetime
from binance.client import Client
from binance.exceptions import BinanceAPIException


def setup_logger(name, log_file, level=logging.INFO):
    """
    Налаштування логування.
    :param name: Ім'я логера
    :param log_file: Шлях до файлу логів
    :param level: Рівень логування
    :return: Налаштований логер
    """
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def load_config(config_file):
    """
    Завантаження конфігурацій з файлу .ini.
    :param config_file: Шлях до конфігураційного файлу
    :return: Об'єкт ConfigParser із завантаженими даними
    """
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


def format_timestamp(timestamp):
    """
    Форматує часову мітку у зручний для читання формат.
    :param timestamp: Часова мітка (як int або float)
    :return: Форматований рядок часу
    """
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def calculate_percentage_change(old_value, new_value):
    """
    Розрахунок відсоткової зміни між двома значеннями.
    :param old_value: Початкове значення
    :param new_value: Нове значення
    :return: Відсоткова зміна
    """
    try:
        change = ((new_value - old_value) / old_value) * 100
        return round(change, 2)
    except ZeroDivisionError:
        return float('inf')


def validate_api_keys(api_key, api_secret):
    """
    Перевірка валідності API ключів через реальний запит до Binance API.
    :param api_key: API ключ
    :param api_secret: API секрет
    :return: True, якщо ключі валідні, інакше False
    """
    if not (api_key and api_secret):
        return False

    try:
        client = Client(api_key, api_secret)
        client.ping()  # Виконуємо тестовий запит до Binance API
        return True
    except BinanceAPIException as e:
        logging.error(f"Невалідні API ключі: {e}")
        return False
    except Exception as e:
        logging.error(f"Помилка під час перевірки API ключів: {e}")
        return False
