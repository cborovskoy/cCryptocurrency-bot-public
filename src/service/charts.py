import plotly.graph_objects as go
import datetime
import pandas as pd

COLOR_BG = '#191b20'


async def make_chart(df: pd.DataFrame) -> bytes:
    is_scatter = df.shape[0] > 1 and (df.index[1] - df.index[0]) == datetime.timedelta(minutes=1)

    if is_scatter:
        figure_data = [go.Scatter(x=df.index, y=df['Close'], line=dict(color='white', width=2))]
    else:
        figure_data = [go.Candlestick(x=df.index, open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'],
                                      increasing_line_color='#02C076', decreasing_line_color='#CF304A')]

    fig = go.Figure(data=figure_data)

    max_price = df['High'].max()
    max_price_date = df['High'].idxmax()
    min_price = df['Low'].min()
    min_price_date = df['Low'].idxmin()
    last_price = df.tail(1)['Close'].item()

    # Узнаём, больше ли последний элемент чем предпоследний
    ratio_of_last_and_penultimate = ''
    for price in df['Close'][::-1]:
        if price != last_price:
            if last_price > price:
                ratio_of_last_and_penultimate = '>'
            else:
                ratio_of_last_and_penultimate = '<'
            break

    direction_annot = {}
    for num, date in enumerate([min_price_date, max_price_date]):
        temp_timedelta = date - (fig.data[0].x[0])
        temp_ax = -15
        temp_xanchor = 'right'
        if temp_timedelta < datetime.timedelta(minutes=8):
            temp_ax = 15
            temp_xanchor = 'left'
        direction_annot['min' if num == 0 else 'max'] = {'ax': temp_ax, 'xanchor': temp_xanchor}

    candlestick_template = go.layout.Template()
    candlestick_template.layout.annotations = [
        # Добавляем ватермарку
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
        # Добавляем указатель на максимальную цену
        dict(
            name='show_max_price',
            text=f"<b>{round(max_price, 2)}<b>",
            x=max_price_date, y=max_price,
            ax=direction_annot['max']['ax'], ay=0,
            xref='x', yref='y', showarrow=True,
            xanchor=direction_annot['max']['xanchor'], yanchor='middle',
            arrowcolor='#7B7F86', font=dict(color='#7B7F86'),
        ),
        # Добавляем указатель на минимальную цену
        dict(
            name='show_min_price',
            text=f"<b>{round(min_price, 2)}<b>",
            x=min_price_date, y=min_price,
            ax=direction_annot['min']['ax'], ay=0,
            xref='x', yref='y', showarrow=True,
            xanchor=direction_annot['min']['xanchor'], yanchor='middle',
            arrowcolor='#7B7F86', font=dict(color='#7B7F86'),
        ),
        # Добавляем указатель на последнюю цену
        dict(
            name='show_last_price',
            text=f"<b>{round(last_price, 2)}<b>",
            x=1.018, y=last_price,
            xref='paper', yref='y',
            font=dict(color='white'),
            showarrow=False, xanchor='left'

        )

    ]

    y_offset_shape = (max_price - min_price) * 0.03
    fig.add_shape(type="path",
                  path=f" M 1.005 {last_price}"
                       f" L 1.02 {last_price + y_offset_shape}"
                       f" L 1.15 {last_price + y_offset_shape}"
                       f" L 1.15 {last_price - y_offset_shape}"
                       f" L 1.02 {last_price - y_offset_shape}"
                       f" Z",
                  line=dict(
                      color="#BB2742" if ratio_of_last_and_penultimate == '<' else '#019362',
                      width=2,
                  ),
                  fillcolor="#A81E3A" if ratio_of_last_and_penultimate == '<' else '#008057',
                  )
    fig.update_shapes(dict(xref='paper', yref='y'))

    fig.update_layout(width=960, height=720,
                      # Меняем цвет фона
                      plot_bgcolor=COLOR_BG,
                      paper_bgcolor=COLOR_BG,
                      # Убираем нижнюю шкалу
                      xaxis_rangeslider_visible=False,
                      # Уменьшаем границы
                      margin=dict(l=0, r=140, t=0, b=55),

                      # Перемещаем шкалу Y вправо и красим + красим сетку + добавляем нижнюю линию
                      yaxis={'side': 'right', 'color': '#5E6673', 'gridcolor': '#1C1F25', 'gridwidth': 2,
                             'showline': True, 'linewidth': 2, 'linecolor': '#2B2F36',
                             'ticklen': 11, 'tickcolor': '#1C1F25', 'tickwidth': 2},

                      # Красим шкалу Х + красим сетку + добавляем правую линию + настраиваем формат
                      xaxis={'color': '#5E6673', 'gridcolor': '#1C1F25', 'gridwidth': 2,
                             'showline': True, 'linewidth': 2, 'linecolor': '#2B2F36',
                             'tickformat': '%H:%M', 'ticklen': 11, 'tickcolor': COLOR_BG},
                      font={'size': 18},
                      template=candlestick_template)

    return fig.to_image(format="png")
