import pandas as pd
import matplotlib.pyplot as plt
import logging

# Создаем логирование
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Чтение CSV файла с разделителем табуляции
file_path = 'Экспозиция ТДСК с 01.07.2023 по 31.12.2023.csv'
df = pd.read_csv(file_path, sep='\t', skiprows=1, names=[
    'id', 'advert_id', 'domain_developer', 'address_gp', 'description',
    'entrance_number', 'floor', 'area', 'room_count', 'flat_number',
    'price', 'published_at', 'actualized_at'])

logging.info('Преобразование столбца actualized_at в datatime формат')
df['actualized_at'] = pd.to_datetime(df['actualized_at'], errors='coerce')

df['actualized_at'] = df['actualized_at'].dt.tz_localize(None)


# Фильтруем данные датой до 31.12.2023
logging.info('Фильтрация данных до 31.12.2023')
df = df[df['actualized_at'] <= '2023-12-31']

# Проверка вывода данных после чтения и преобразования
logging.info("Начальные данные:")
print(df.head())

logging.info('Заполнение данных для каждого дня в рассматриваемом периоде')
date_range = pd.date_range(start='2023-07-01', end='2023-12-31')
addresses = df['address_gp'].unique()

# Создание DataFrame для формирования сводной таблицы
summary_df = pd.DataFrame([(date, address) for date in date_range for address in addresses], columns=['date', 'address'])

logging.info('Объединение таблиц и расчет активных квартир')
summary_df = summary_df.merge(df[['address_gp', 'actualized_at']], left_on='address', right_on='address_gp', how='left')

# Определяем количество активных квартир на каждый день
summary_df['active'] = summary_df['actualized_at'] >= summary_df['date']

# Группировка данных по дате и адресу, подсчитываем активные квартиры
pivot_table = summary_df.groupby(['date', 'address']).agg(active_apartments=('active', 'sum')).reset_index()

logging.info('Сохранение сводной таблицы в CSV')
pivot_table.to_csv('summary_table.csv', index=False)

logging.info('Сохранение сводной таблицы в XLSX')
pivot_table.to_excel('summary_table.xlsx', index=False)

# Группировка по месяцам и количеству комнат
df['month'] = df['actualized_at'].dt.to_period('M')
monthly_summary = df.groupby(['month', 'room_count']).size().unstack(fill_value=0)

logging.info("Сводные данные за месяц:")
print(monthly_summary.head())

# Проверяем не пустой ли DataFrame для построения графика
if monthly_summary.empty:
    logging.error("Нет данных для построения графика. Пожалуйста, ознакомьтесь с вводимыми данными и этапами обработки")
else:
    logging.info("Построение графика")
    ax = monthly_summary.plot(kind='bar', stacked=True, figsize=(12, 8), colormap='viridis')
    ax.set_title('Количество активных квартир в месяц, в разбивке по количеству комнат (с 01.07.2023 по 31.12.2023)')
    ax.set_xlabel('Месяц')
    ax.set_ylabel('Количество активных квартир')
    ax.legend(title='Комнат')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('monthly_summary.png')
    plt.show()

