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
