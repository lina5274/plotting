import matplotlib.pyplot as plt
import plotly.graph_objects as go
import pandas as pd

def calculate_std_dev(data):
    """
    Вычисляет стандартное отклонение закрытия цены акции.
    
    Parameters:
    - data (pandas.DataFrame): Данные о цене акции.
    
    Returns:
    - float: Стандартное отклонение.
    """
    std_dev = data['Close'].std()
    return std_dev

def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    """
    Создает и сохраняет график цен акций с возможностью отображения стандартного отклонения.
    
    Parameters:
    - data (pandas.DataFrame): Данные о цене акции.
    - ticker (str): Тикер акции.
    - period (str): Период наблюдения.
    - filename (str, optional): Имя файла для сохранения графика. По умолчанию None.
    - style (str): Стиль графика.
    """
    plt.style.use(style)
    fig = go.Figure()  # Исправлено: добавлено создание объекта Figure из Plotly

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            fig.add_trace(go.Scatter(x=dates, y=data['Close'], mode='lines', name='Close Price'))
            fig.add_trace(go.Scatter(x=dates, y=data['Moving_Average'], mode='lines', name='Moving Average'))
            if True:  # Предполагается, что всегда нужно показывать стандартное отклонение
                std_dev = calculate_std_dev(data)
                fig.add_shape(type="line", x0=min(dates), x1=max(dates), y0=std_dev, y1=std_dev, line=dict(color="Red", dash="dash"), name=f'Std Dev ({std_dev:.2f})')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], mode='lines', name='Close Price'))
        fig.add_trace(go.Scatter(x=data['Date'], y=data['Moving_Average'], mode='lines', name='Moving Average'))

    fig.update_layout(title_text=f"{ticker} Цена акций с течением времени",
                      xaxis_title="Дата",
                      yaxis_title="Цена",
                      legend_title="Серия данных")

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"
    
    fig.write_html(filename)
    print(f"Интерактивный график сохранен как {filename}")

def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет о сильных колебаниях цены акций.
    
    Parameters:
    - data (pandas.DataFrame): Данные о цене акции.
    - threshold (float): Порог колебаний цены.
    """
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    pr = max_price - min_price

    if pr > threshold:
        print(f"Цена акций колебалась более чем на {threshold}% за период")
    else:
        print("Цена акций не колебалась на указанный процент за период")
