import pandas as pd
import os
import re

def split_files(dir, file_pattern = r'\*.csv'):
    # Чтение исходного CSV-файла с пропуском ошибочных строк и указанием кодировки
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and 'csv' in f]
    print(files)
    file_path = files[0]
    os.chdir(dir)
    try:
        df = pd.read_csv(file_path, encoding='utf-8', sep=';')
    except pd.errors.ParserError as e:
        print(f"Ошибка чтения CSV: {e}")
        raise

    chunk_size = 50
    num_chunks = (len(df) + chunk_size - 1) // chunk_size

    # Разделение DataFrame на части и запись в отдельные файлы
    for i in range(num_chunks):
        start_row = i * chunk_size
        end_row = (i + 1) * chunk_size
        chunk_df = df[start_row:end_row]

        # Запись части в новый CSV-файл с указанием кодировки
        output_file_path = f'{i + 1}_{file_path}'
        chunk_df.to_csv(output_file_path, index=False, encoding='utf-8', sep=';')

        print(f'Часть {i + 1} записана в файл {output_file_path}')

    # Удаление исходного файла
    os.remove(file_path)
    print(f'Исходный файл {file_path} удален')


# split_files()
