import time
import datetime
from src.db.db_preparation import ensure_connection


@ensure_connection
def add_price_sql(conn, price: float, date_time_now: datetime.datetime):
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO price_base (price, date_time) VALUES (?, ?)',
              (str(price), str(date_time_now)))
    conn.commit()

    # Удаляем старые записи
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
    previous_sec = 0
    while True:
        add_price_sql()
        sec = datetime.datetime.utcnow().second
        while sec == previous_sec:
            sec = datetime.datetime.utcnow().second
            time.sleep(0.01)
        previous_sec = sec
        time.sleep(0.1)


if __name__ == '__main__':
    main()
