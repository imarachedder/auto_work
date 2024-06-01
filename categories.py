import pandas as pd
import os
import shutil
from transliterate import translit


def review_order(dir, counter=0):
    print(dir, counter)
    if 'VK2_' in dir and os.path.isdir(dir):
        current_dir = os.getcwd()
        print(current_dir)
        matching_files = [f for f in os.listdir(current_dir) if 'Статус аккаунтов' in f]
        if matching_files:
            file_to_read = matching_files[0]
            print(file_to_read)
            print(f"Найден файл: {file_to_read}")
            df = pd.read_excel(file_to_read)
            df = df[df['Статус'] == 'Жив']
            with open(os.path.join(f"{dir}/order.txt"), "r+") as f:
                content = f.read()
                cleaned_content = content.replace('\n', '').split(':')
                cleaned_content[0] = str(df['Логин'].iloc[counter])
                cleaned_content[1] = df['Токен'].iloc[counter]
                print()
                print("review_order", cleaned_content)
            with open(os.path.join(f"{dir}/order.txt"), "w") as f:
                for i, el in enumerate(cleaned_content):
                    if i == len(cleaned_content) - 1:
                        f.write(f"{el}")
                    else:
                        f.write(f"{el}:")
            df.to_excel(file_to_read, index=False)


def refactor_settings(dir_name, new_file_name):
    with open(os.path.join(f"{dir_name}/setting.txt"), "r+") as f:
        content = f.read()
        cleaned_content = content.split('\n')
        cleaned_content[5] = new_file_name
        print(cleaned_content)

    with open(os.path.join(f"{dir_name}/setting.txt"), "w") as f:
        for i, el in enumerate(cleaned_content):
            f.write(f"{el}\n")

def transtale_file(dir_name, file_name):
    for file in os.listdir('Готовые файлы'):
        if file_name == file:
            # Разделить имя файла и его расширение
            file_base, file_ext = os.path.splitext(file)
            file_path = os.path.join(f"Готовые файлы/{file}")
            transliterated_name = translit(file_base, 'ru', reversed=True)
            new_file_name = transliterated_name + file_ext
            # Полный путь к новому файлу
            new_file_path = os.path.join(f'{dir_name}/{new_file_name}')
            # Переименовать файл
            # os.rename(file_path, new_file_path)
            shutil.copy(file_path, new_file_path)

            refactor_settings(dir_name, new_file_name)
            # with open(os.path.join(f"{dir_name}/setting.txt"), "r+") as f:
            #     content = f.read()
            #     cleaned_content = content.split('\n')
            #     cleaned_content[5] = new_file_name
            #     print(cleaned_content)
            #
            # with open(os.path.join(f"{dir_name}/setting.txt"), "w") as f:
            #     for i, el in enumerate(cleaned_content):
            #             f.write(f"{el}\n")
            # print(file)
            # print(file_path)
            # print(file_base, file_ext)
            # print(new_file_path)

def refactor_files():
    for dir in os.listdir():
        # print("1.", dir)
        if 'VK2_' in dir and os.path.isdir(dir):
            # print("2.", dir)
            for file in os.listdir('Готовые файлы'):
                # print("3.", file)
                if dir == f"VK2_{file.split('.')[0]}":
                    # print(f"4. VK2_{file.split('.')[0]}")
                    # логика : если директория равна VK2_полное название категории тогда выполняется
                    # например : VK2_зубная щетка (БЕЗ НИЖНИХ ПОДЧЕРКИВАНИЙ МЕЖДУ СЛОВАМИ)
                    # ОБЯЗАТЕЛЬНО ВСЕ С МАЛЕНЬКОЙ БУКВЫ)
                    transtale_file(dir, file)
                    # review_order(dir)
                    df = pd.read_excel('промпты.xlsx')
                    # print(file)
                    for i in range(len(df)):
                        if file.split('.')[0] == str(df['Категория'].iloc[i]).lower():
                            with open(os.path.join(f"{dir}/order.txt"), "r+") as f:
                                content = f.read()
                                cleaned_content = content.replace('\n', '').split(':')
                                cleaned_content[2] = df['Комментарий'].iloc[i]
                                print(cleaned_content)

                            with open(os.path.join(f"{dir}/order.txt"), "w") as f:
                                for j, el in enumerate(cleaned_content):
                                    if j == len(cleaned_content) - 1:
                                        f.write(f"{el}")
                                    else:
                                        f.write(f"{el}:")
                            # print(dir)

# refactor_files()