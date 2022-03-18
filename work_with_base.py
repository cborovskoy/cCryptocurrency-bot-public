import sqlite3
import requests
import time
import datetime
from settings import COINDESK_API_URL, get_base_path


def ensure_connection(func):
    """ Декоратор для подключения к СУБД: открывает соединение,
        выполняет переданную функцию и закрывает за собой соединение.
        Потокобезопасно!
    """

    def inner(*args, **kwargs):
        with sqlite3.connect(get_base_path()) as conn:
            kwargs['conn'] = conn
            res = func(*args, **kwargs)
        return res

    return inner


@ensure_connection
def init_db(conn, force: bool = False):
    """ Проверить что нужные таблицы существуют, иначе создать их

        Важно: миграции на такие таблицы вы должны производить самостоятельно!

        :param conn: подключение к СУБД
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


@ensure_connection
def add_price_sql(conn):
    # Запрос информации о цене
    response = requests.get(COINDESK_API_URL).json()
    price = response['bpi']['USD']['rate_float']
    date_time = datetime.datetime.utcnow()
    # Запись в базу информации о цене
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO price_base (price, date_time) VALUES (?, ?)', (price, str(date_time)))
    conn.commit()


@ensure_connection
def del_price_sql(conn):
    c = conn.cursor()
    num_of_rows = c.execute('SELECT COUNT(*) FROM price_base;').fetchone()[0]
    if num_of_rows >= 86400:
        c.execute('DELETE FROM price_base WHERE rowid in (select rowid FROM price_base LIMIT 1)')
    conn.commit()


@ensure_connection
def get_all_data(conn):
    c = conn.cursor()

    temp = True
    while temp:
        dates_times_lst = [job[0] for job in c.execute("SELECT date_time FROM price_base")]
        prices_lst = [job[0] for job in c.execute("SELECT price FROM price_base")]
        if len(dates_times_lst) == len(prices_lst):
            temp = False
            all_data = {"price": prices_lst, 'date': dates_times_lst}
    return all_data


@ensure_connection
def get_price_now(conn):
    c = conn.cursor()
    return c.execute("SELECT * FROM price_base ORDER BY id desc limit 1;")


def main():
    init_db()
    previous_sec = 0
    while True:
        add_price_sql()
        print('add_price - done')
        del_price_sql()
        sec = datetime.datetime.utcnow().second
        while sec == previous_sec:
            sec = datetime.datetime.utcnow().second
            time.sleep(0.01)
        previous_sec = sec
        time.sleep(0.1)


if __name__ == '__main__':
    main()
