import matplotlib.pyplot as plt
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
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            if show_std_dev:
                std_dev = calculate_std_dev(data)
                plt.axhline(y=std_dev, color='r', linestyle='--', label=f'Std Dev ({std_dev:.2f})')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")

def notify_if_strong_fluctuations(data, threshold):
    max_price = data['Close'].max()
    min_price = data['Close'].min()

    pr = max_price - min_price

    if pr > threshold:
        print(f"Цена акций колебалась более чем на {threshold}% за период")
    else:
        print("Цена акций не колебалась на указанный процент за период")

