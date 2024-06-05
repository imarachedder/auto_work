import os
import time
from check import check_parse
from barkov import parseBarkov
from get_views_from_post import coverage_parse
from categories import refactor_files, review_order, refactor_settings
from vk import vk_posting
from cute_files_to_dirs import archive
import pandas as pd
from test import split_files


def main():
    print("=" * 40)
    print("1. Сбор информации начат")
    print("=" * 40)
    check_parse()
    print("=" * 40)
    print("1. Сбор информации окончен")
    print("=" * 40)
    time.sleep(60)
    print("=" * 40)
    print("2. Начинаю выполнение функции parseBarkov")
    print("=" * 40)
    parseBarkov()
    print("=" * 40)
    print("2. parseBarkov закончил работу")
    print("=" * 40)
    time.sleep(60)
    print("=" * 40)
    print("3. Начинаю выполнение функции coverage_parse")
    print("=" * 40)
    coverage_parse()
    print("=" * 40)
    print("3. Закончил выполнение функции coverage_parse")
    print("=" * 40)
    time.sleep(10)
    print("=" * 40)
    print("4. Начинаю предобработку")
    print("=" * 40)
    refactor_files()
    print("=" * 40)
    print("3. Закончил предобработку")
    print("=" * 40)
    os_dir = os.getcwd()
    try:
        df = pd.read_excel('settings_barkov.xlsx', index_col=False)
        df_group = df.groupby('Категория').count().reset_index()
        df_group['Категория'] = df_group['Категория'].str.lower()
        # print(df_group)
        for dir in os.listdir():
            # print(dir)
            # print('VK2_' in dir, f"{dir[4:]}.csv" in os.listdir('Готовые файлы'))
            if 'VK2_' in dir and os.path.isdir(dir) and f"{dir[4:]}.csv" in os.listdir('Готовые файлы') and dir[4:] in df_group['Категория'].values:
                # print("DDDD")
                split_files(dir=dir)
                print("split_files закончил работу")
                print(os.getcwd())
                os.chdir(os_dir)
                files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and 'csv' in f]
                print("files закончил работу")
                for i, file in enumerate(files):
                    print("я в цикле закончил работу")
                    review_order(dir=dir, counter=i)
                    refactor_settings(dir_name=dir, new_file_name=file)
                    print(f"{i+1} review_order закончил работу")

                    vk_posting(dir, file)
                    print(f"{i+1} vk_posting закончил работу")
                    os.chdir(os_dir)
    except Exception as e:
        print(f"Возникла ошибка при постинке комментариев: {e}")
    finally:
        # Перемещаем ненужные файлы файлы в архив
        os.chdir(os_dir)
        archive()
        print()

if __name__ == "__main__":
    main()



