import os
import shutil
import datetime

def archive():
    print("Добавляем ненужные файлы в архив")

    # Создание директорий, если они не существуют
    if not os.path.exists("Архив просмотры"):
        os.makedirs("Архив просмотры")

    if not os.path.exists("Архив статус аккаунтов"):
        os.makedirs("Архив статус аккаунтов")

    # Проход по файлам в текущей директории
    for file in os.listdir():
        if os.path.isfile(file):
            destination = ""
            if 'просмотры' in file:
                destination = 'Архив просмотры'
            elif 'Статус аккаунтов' in file:
                destination = 'Архив статус аккаунтов'

            if destination:
                base, extension = os.path.splitext(file)
                new_name = file
                counter = 1

                # Если файл с таким именем уже существует, добавляем метку времени или счетчик
                while os.path.exists(os.path.join(destination, new_name)):
                    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                    new_name = f"{base}_{timestamp}{extension}"
                    counter += 1

                # Перемещение файла в целевую директорию
                shutil.move(file, os.path.join(destination, new_name))

    print("Файлы успешно перемещены")


# Пример вызова функции
# archive()
