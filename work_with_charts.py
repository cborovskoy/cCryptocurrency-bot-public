from multiprocessing import Process
import plotly.graph_objects as go
import pandas as pd
import datetime
import time
from work_with_df import get_configured_df_and_data_info
from work_with_files import delete_old_charts
from settings import CT_LINE, CT_CANDLESTICK, LABEL_TIME, LABEL_1M, LABEL_15M, LABEL_1H, get_path_chart

COLOR_BG = '#191b20'

print('Posle importa')

def make_chart(chart_type: str, candle_time=None):

    print('make_chart')
    chart_path = None

    time_intervals = {
        None: 2,
        '1T': 2,
        '15T': 30,
        '1H': 100
    }


    paphs_chart = {
        # None: PATH_CHART_TIME,
        # '1T': PATH_CHART_1M,
        # '15T': PATH_CHART_15M,
        # '1H': PATH_CHART_1H,
        None: get_path_chart(LABEL_TIME),
        '1T': get_path_chart(LABEL_1M),
        '15T': get_path_chart(LABEL_15M),
        '1H': get_path_chart(LABEL_1H),
    }

    if chart_type == CT_CANDLESTICK:

        df, data_info = get_configured_df_and_data_info(chart_type=chart_type,
                                                        candle_time=candle_time,
                                                        time_interval=time_intervals[candle_time])

        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                             open=df['open'], high=df['high'],
                                             low=df['low'], close=df['close'],
                                             increasing_line_color='#02C076',
                                             decreasing_line_color='#CF304A')])

    elif chart_type == CT_LINE:
        df, data_info = get_configured_df_and_data_info(chart_type=chart_type, time_interval=2)
        fig = go.Figure([go.Scatter(x=df['Date'], y=df['price'], line=dict(color='white', width=2))])

    direction_annot = {}
    for i in ['min', 'max']:
        temp_date_time = str(data_info[f'{i}_price_date'])
        price_date = datetime.datetime(int(temp_date_time[:4]), int(temp_date_time[5:7]), int(temp_date_time[8:10]),
                                       int(temp_date_time[11:13]), int(temp_date_time[14:16]), 0)

        temp_timedelta = price_date - (fig.data[0].x[0])
        temp_ax = -15
        temp_xanchor = 'right'
        if temp_timedelta < datetime.timedelta(minutes=8):
            temp_ax = 15
            temp_xanchor = 'left'
        direction_annot[i] = {'ax': temp_ax, 'xanchor': temp_xanchor}

    candlestick_template = go.layout.Template()
    candlestick_template.layout.annotations = [
        # ?????????????????? ????????????????????
        dict(
            name="draft watermark",
            text="<b>ccryptocurrency_bot</b>",
            opacity=0.02,
            font=dict(color="white", size=64),
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        ),
        # ?????????????????? ?????????????????? ???? ???????????????????????? ????????
        dict(
            name='show_max_price',
            text=f"<b>{round(data_info['max_price'], 2)}<b>",
            x=data_info['max_price_date'], y=data_info['max_price'],
            ax=direction_annot['max']['ax'], ay=0,
            xref='x', yref='y', showarrow=True,
            xanchor=direction_annot['max']['xanchor'], yanchor='middle',
            arrowcolor='#7B7F86', font=dict(color='#7B7F86'),
        ),
        # ?????????????????? ?????????????????? ???? ?????????????????????? ????????
        dict(
            name='show_min_price',
            text=f"<b>{round(data_info['min_price'], 2)}<b>",
            x=data_info['min_price_date'], y=data_info['min_price'],
            ax=direction_annot['min']['ax'], ay=0,
            xref='x', yref='y', showarrow=True,
            xanchor=direction_annot['min']['xanchor'], yanchor='middle',
            arrowcolor='#7B7F86', font=dict(color='#7B7F86'),
        ),
        # ?????????????????? ?????????????????? ???? ?????????????????? ????????
        dict(
            name='show_last_price',
            text=f"<b>{round(data_info['last_price'], 2)}<b>",
            x=1.018, y=data_info['last_price'],
            xref='paper', yref='y',
            font=dict(color='white'),
            showarrow=False, xanchor='left'

        )

    ]

    y_offset_shape = (data_info['max_price'] - data_info['min_price']) * 0.03
    fig.add_shape(type="path",
                  path=f" M 1.005 {data_info['last_price']}"
                       f" L 1.02 {data_info['last_price'] + y_offset_shape}"
                       f" L 1.15 {data_info['last_price'] + y_offset_shape}"
                       f" L 1.15 {data_info['last_price'] - y_offset_shape}"
                       f" L 1.02 {data_info['last_price'] - y_offset_shape}"
                       f" Z",
                  line=dict(
                      color="#BB2742" if data_info['ratio_of_last_and_penultimate'] == '<' else '#019362',
                      width=2,
                  ),
                  fillcolor="#A81E3A" if data_info['ratio_of_last_and_penultimate'] == '<' else '#008057',
                  )
    fig.update_shapes(dict(xref='paper', yref='y'))

    fig.update_layout(width=960, height=720,
                      # ???????????? ???????? ????????
                      plot_bgcolor=COLOR_BG,
                      paper_bgcolor=COLOR_BG,
                      # ?????????????? ???????????? ??????????
                      xaxis_rangeslider_visible=False,
                      # ?????????????????? ??????????????
                      margin=dict(l=0, r=140, t=0, b=55),

                      # ???????????????????? ?????????? Y ???????????? ?? ???????????? + ???????????? ?????????? + ?????????????????? ???????????? ??????????
                      yaxis={'side': 'right', 'color': '#5E6673', 'gridcolor': '#1C1F25', 'gridwidth': 2,
                             'showline': True, 'linewidth': 2, 'linecolor': '#2B2F36',
                             'ticklen': 11, 'tickcolor': '#1C1F25', 'tickwidth': 2},

                      # ???????????? ?????????? ?? + ???????????? ?????????? + ?????????????????? ???????????? ?????????? + ?????????????????????? ????????????
                      xaxis={'color': '#5E6673', 'gridcolor': '#1C1F25', 'gridwidth': 2,
                             'showline': True, 'linewidth': 2, 'linecolor': '#2B2F36',
                             'tickformat': '%H:%M', 'ticklen': 11, 'tickcolor': COLOR_BG},
                      font={'size': 18},
                      template=candlestick_template)

    # fig.show()
    date_time_now = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    chart_path = paphs_chart[candle_time]
    fig.write_image(f'{chart_path}/btc_usd_{date_time_now}-{round(data_info["last_price"], 2)}.png')
    delete_old_charts(path=chart_path)
    print(f'{chart_path} is done')


def start_cyclic_charts_gen(chart_type: str, candle_time=None):
    print('start_cyclic_charts_gen')
    while True:
        make_chart(chart_type=chart_type, candle_time=candle_time)
        time.sleep(1)


def main():
    print('startanuli')
    th_time_chart = Process(target=start_cyclic_charts_gen, args=(CT_LINE,))
    th_1m_chart = Process(target=start_cyclic_charts_gen, args=(CT_CANDLESTICK, '1T'))
    th_15m_chart = Process(target=start_cyclic_charts_gen, args=(CT_CANDLESTICK, '15T'))
    th_1h_chart = Process(target=start_cyclic_charts_gen, args=(CT_CANDLESTICK, '1H'))

    th_time_chart.start()
    th_1m_chart.start()
    th_15m_chart.start()
    th_1h_chart.start()

    th_time_chart.join()
    th_1m_chart.join()
    th_15m_chart.join()
    th_1h_chart.join()



if __name__ == '__main__':
    main()
