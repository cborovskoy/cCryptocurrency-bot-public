import sqlite3
from pathlib import PurePath, Path
from src.config import load_config


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        config_path = PurePath(Path(__file__).parents[2], 'bot.ini')
        config = load_config(config_path)
        base_path = ('../' if __name__ == '__main__' else '') + config.db.path

        with sqlite3.connect(base_path) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: Подключение к СУБД
        :param force: явно пересоздать все таблицы
    """
    c = conn.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS price_base')

    c.execute(f'''
        CREATE TABLE IF NOT EXISTS price_base (
            id          INTEGER PRIMARY KEY,
            date_time   TEXT,
            price       REAL DEFAULT 0.0
        )
    ''')

    # Сохранить изменения
    conn.commit()
