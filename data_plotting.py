import plotly.graph_objects as go
import pandas as pd

def calculate_std_dev(data):
    std_dev = data['Close'].std()
    return std_dev
    
def create_and_save_plot(data, ticker, period, filename=None, style='default'):
    plt.style.use(style)
    plt.figure(figsize=(10, 6))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            fig.add_trace(go.Scatter(x=dates, y=data['Close'], mode='lines', name='Close Price'))
            fig.add_trace(go.Scatter(x=dates, y=data['Moving_Average'], mode='lines', name='Moving Average'))
            if show_std_dev:
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
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    pr = max_price - min_price

    if pr > threshold:
        print(f"Цена акций колебалась более чем на {threshold}% за период")
    else:
        print("Цена акций не колебалась на указанный процент за период")

