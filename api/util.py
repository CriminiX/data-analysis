import logging

import numpy as np
from settings import get_settings
from datetime import date
import unicodedata

def get_logger(name):
    logger = logging.getLogger(name)
    settings = get_settings()
    level = logging.DEBUG if settings.debug else logging.INFO
    logger.setLevel(level)
    formatter = logging.Formatter(
        (
        '{"unix_time": %(created)s, "time": "%(asctime)s", "module": "%(name)s",'
        ' "lineno": %(lineno)s, "level": "%(levelname)s", "msg": "%(message)s"}'
        )
    )
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(level)
    logger.addHandler(handler)
    return logger

def clone_log_config(base_logger: logging.Logger, target_logger: logging.Logger):
    target_logger.handlers.clear()
    target_logger.addHandler(base_logger.handlers[0])
    target_logger.setLevel(base_logger.level)

def season_by_day(day: date):
    return ((day.month % 12) // 3) + 1

def shift_by_hour(hour: int):
    if hour >= 0 and hour < 8:
        return 0
    elif hour >= 8 and hour < 16:
        return 1
    else:
        return 2

def sin_transform(x, period):
    return np.sin(x / period * 2 * np.pi)

def cos_transform(x, period):
    return np.cos(x / period * 2 * np.pi)

def remove_special_chars(text: str):
    text = unicodedata.normalize('NFD', text) \
        .encode('ascii', 'ignore') \
        .decode("utf-8")
    return str(text)

def replace_saint_names(text: str):
    saint_names = ['sao ', 'sto ', 'santa ', 'santo ',  's. ']
    
    for saint in saint_names:
        text = text.replace(saint, 's.')
        if text.startswith(saint.strip()):
            text = text.replace(saint.strip(), 's.')

    return text