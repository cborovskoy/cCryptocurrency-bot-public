import pandas as pd
from work_with_base import get_all_data
import datetime

from collections import OrderedDict
from settings import CT_CANDLESTICK, CT_LINE, CT_5MINUTES_TEST


def get_configured_df_and_data_info(chart_type: str, time_interval=None, candle_time=None):
    """
    :param chart_type:
    :param time_interval: Measured in hours
    :param candle_time:
    :return:
    """

    df = pd.DataFrame(get_all_data())
    temp_df = None

    # Теперь столбец с датой в формате datetime
    datetime_lst = []
    for i in df['date']:
        datetime_obj = datetime.datetime(int(i[:4]), int(i[5:7]), int(i[8:10]),
                                         int(i[11:13]), int(i[14:16]), int(i[17:19]))
        datetime_lst.append(datetime_obj)
    df['date_time'] = datetime_lst

    last_hour = df['date_time'].to_list()[-1] - datetime.timedelta(hours=time_interval)
    df = df.loc[df['date_time'] > last_hour]

    if chart_type == CT_LINE:
        temp_df = df
        temp_df.pop('date')
        temp_df.rename(columns={'date_time': 'Date'}, inplace=True)


    elif chart_type == CT_CANDLESTICK:
        temp_df = df
        temp_df.pop('date')
        temp_df.rename(columns={'date_time': 'Date'}, inplace=True)
        # print(temp_df)
        temp_df.set_index('Date')

        temp_df['open'] = temp_df['price']
        temp_df['high'] = temp_df['price']
        temp_df['low'] = temp_df['price']
        temp_df['close'] = temp_df['price']

        temp_df = temp_df. \
            resample(candle_time, on='Date'). \
            agg(OrderedDict([('open', 'first'),
                             ('high', 'max'),
                             ('low', 'min'),
                             ('close', 'last'),
                             ])
                )
        temp_df.reset_index(inplace=True)

    data_info = {}
    data_info['num_of_rows'] = df.shape[0]
    data_info['max_price'] = max(df['price'].to_list())
    data_info['max_price_date'] = df.loc[df['price'] == data_info['max_price'], 'Date'].iloc[0]
    data_info['min_price'] = min(df['price'].to_list())
    data_info['min_price_date'] = df.loc[df['price'] == data_info['min_price'], 'Date'].iloc[0]
    data_info['last_price'] = df['price'].to_list()[-1]

    # Узнаём, больше ли последний элемент чем предпоследний
    ratio_of_last_and_penultimate = ''
    for price in df['price'][::-1]:
        if price != data_info['last_price']:
            if data_info['last_price'] > price:
                ratio_of_last_and_penultimate = '>'
            else:
                ratio_of_last_and_penultimate = '<'
            break
    data_info['ratio_of_last_and_penultimate'] = ratio_of_last_and_penultimate

    return [temp_df, data_info]


def main():
    df, data_info = get_configured_df_and_data_info(chart_type=CT_5MINUTES_TEST, candle_time='1T', time_interval=1)
    print(df)


if __name__ == '__main__':
    main()
