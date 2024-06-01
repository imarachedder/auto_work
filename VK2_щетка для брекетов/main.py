import random
#import sys
import httpx
import requests
from selenium import webdriver
import time
import os
import vk_api
from selenium.webdriver.common.by import By
import datetime
import csv
import openai
import threading

ev = threading.Event()


def start_acc_post(acc):  # разбиваем работу аккаунтов на потоки
    global urls
    #sys.stdout.write('Поток запущен')
    for url in urls:
        #try:
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Взята ссылка - {url[0]}")
        url_create = url[0].split('wall')[1]  # 114005536_47613
        user_id, post_id = url_create.split('_')
        api_token = set[4]
        #print(set[7])
        #print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Создание сессии OpenAI")
        client = openai.OpenAI(
            api_key=api_token,
            http_client=httpx.Client(proxies=set[7])
        )
        #print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Сессия создана")
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Генерация комментария")
        if len(url[1]) < 2000:
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "user", "content": f"Действуй как специалист по крауд-маркетингу, играющий роль {acc[1]}. Напиши комментарий для поста Вконтакте. Твой ответ длиной 30-50 слов. Ты пишешь на русском языке. Твой ответ не должен быть в кавычках. - '{url[1]}'"}
                ]
            )
            #print(completion)
            # обращение к ChatGTP
        else:
            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Пост укорочен")
            completion = client.chat.completions.create(
                model="gpt-3.5-turbo-16k",
                messages=[
                    {"role": "user", "content": f"Действуй как специалист по крауд-маркетингу, играющий роль {acc[1]}. Напиши комментарий для поста Вконтакте. Твой ответ длиной 20-30 слов. Ты пишешь на русском языке. Твой ответ не должен быть в кавычках. - '{url[1][:2000]}'"}
                ]
            )
            #print(completion)
            # обращение к ChatGTP
        #print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Вызов функции отправки")
        send_comment(acc[0], completion.choices[0].message.content, user_id, post_id,
                     url[0])  # Оставляем комментарий
        #except Exception as ex:
            #print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] f{ex} вввв")
        if '-' not in acc[-1]:
            time.sleep(int(acc[-1]))
        else:
            a, b = acc[-1].split('-')
            time.sleep(random.randint(int(a), int(b)))
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Запись комментария в базу")
        with open('comments.txt', "w") as file:  # Обновляем список комментариев
            file.writelines("%s\n" % line for line in com)


def send_comment(acc, comment_text, user_id, post_id, url):  # чтобы отправить комментарии
    try:
        #print(comment_text)
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Отправка комментария для {url}")
        acc.wall.createComment(owner_id=user_id, post_id=post_id, message=comment_text)
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Комментарий отправлен для {url}")
        if url not in com:
            com.append(url)
    except vk_api.exceptions.ApiError as e:
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}]Ошибка отправки комментария для {url}:", e)

with open("comments.txt", 'r', encoding='utf8') as file:  # считываем готовые ссылки на посты
    com = file.read().split('\n')
with open('setting.txt', 'r', encoding='utf8') as file:  # считываем настройки
    set = file.read().split('\n')

if set[5] == '-' or set[5] == "<название файла в формате *.csv/Если файла ставим '-'>":  # проверяем используем парсер или готовый файл
    text = set[0]
    print('Регистрация в Вк')
    phone = set[1]
    password = set[2]
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Начинаем парсер")
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://vk.barkov.net/auth.aspx')  # запускаем парсер
    time.sleep(10)  # vkuiInput__el

    inp = driver.find_elements(By.CLASS_NAME, 'vkuiInput__el')[0]
    inp.clear()
    inp.send_keys(phone)

    time.sleep(10)  # vkuiButton__content vkuiText vkuiText--sizeY-compact vkuiText--w-2

    try:
        btn = driver.find_element(By.CLASS_NAME,
                                  'vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse'.replace(
                                      ' ', '.'))
        btn.click()
        time.sleep(25)

        inp = driver.find_elements(By.NAME, 'password')[0]
        inp.clear()
        inp.send_keys(password)

        time.sleep(3)  # vkuiButton__content vkuiText vkuiText--sizeY-compact vkuiText--w-2

        btn = driver.find_element(By.CLASS_NAME,
                                  'vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse'.replace(
                                      ' ', '.'))
        btn.click()
        time.sleep(60)
    except Exception as ex:
        inp = driver.find_elements(By.NAME, 'password')[0]
        inp.clear()
        inp.send_keys(password)

        time.sleep(3)  # vkuiButton__content vkuiText vkuiText--sizeY-compact vkuiText--w-2
        try:
            btn = driver.find_element(By.CLASS_NAME,
                                      'vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse'.replace(
                                          ' ', '.'))
            btn.click()
            time.sleep(60)
        except Exception as ex:
            pass

    driver.get('https://vk.barkov.net/newsfeed.aspx')
    time.sleep(30)

    inp = driver.find_elements(By.CLASS_NAME, 'form-control')[1]
    inp.clear()
    inp.send_keys(text)

    time.sleep(10)

    btn = driver.find_element(By.ID, 'submitNewsFeed'.replace(' ', '.'))
    btn.click()
    time.sleep(60)

    btns = driver.find_elements(By.CLASS_NAME, 'btn btn-primary'.replace(' ', '.'))  # скачиваем файл
    for i in btns:
        if i.text.strip() == 'Скачать CSV (для Excel)':
            i.click()

    time.sleep(60)

    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Файл получен")
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Считываем файл")

    # name_excel = ''  # ищем название нужного файла
    for i in os.listdir():
        if 'csv' in i:
            name_excel = i
            break

    urls = []
    with open(name_excel, encoding='utf-8') as r_file:  # считываем скаченный файл
        file_reader = csv.reader(r_file, delimiter=";")
        for row in list(file_reader)[1:]:
            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Получена ссылка - {row[0]}")
            urls.append([row[0], row[5]])

    try:
        os.remove(f'./{name_excel}')  # удаляем скаченный файл
    except Exception as ex:
        pass

else:
    urls = []
    with open(set[5], encoding='utf-8') as r_file:  # считываем готовый файл
        file_reader = csv.reader(r_file, delimiter=";")
        for row in list(file_reader)[1:]:
            try:
                urls.append([row[0], row[5]])
                print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Получена ссылка - {row[0]}")
            except Exception as ex:
                print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Не удалось получить ссылку")

print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Ссылки собраны")

time_sleep = set[3]

print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Подключение аккаунтов")

data = []

with open('order.txt', 'r', encoding='utf8') as file:  # считываем информацию про аккаунты
    for line in file.read().split('\n'):
        data.append(line.split(':'))

with open('proxy.list', 'a+', encoding='utf-8') as f:
    proxies = f.read().strip().split("\n")


acc = []
for i in data:  # подключаемся к аккаунтам
    try:
        if len(proxies):
            rq_session = requests.Session()
            rq_session.proxies = {'http': random.choice(proxies)}
            session = vk_api.VkApi(token=i[1], session=rq_session)
        else:
            session = vk_api.VkApi(token=i[1])
        vk = session.get_api()
        acc.append([vk, i[2], i[1], i[3]])
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Подключен аккаунт с номером {i[0]}")
    except Exception as ex:
        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Ошибка подключения аккаунт с номером {i[0]} - {ex}")

if not acc:
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Подключенных аккаунтов не найдено")
    exit()

api_token = set[4]
client = openai.OpenAI(
            api_key=api_token,
            http_client=httpx.Client(proxies=set[7])
)
if set[6] == '2':
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Отбираем нужные посты")
    res = []
    for i in urls:  # отсеиваем посты с помощью ChatGPT
        try:
            if len(i[1]) < 4000:
                completion = client.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "user", "content": f"Take a deep breath. Read the post {i[1]}. If the post is in Russian and discusses or advertises a product then answer Да, otherwise Нет. Reply only Да or Нет"}
                    ]
                )
                print(completion)
                if 'да' in completion.choices[0].message.content.lower().split():
                    res.append(i)
                    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Пост подходит - {i[0]}")
                else:
                    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Пост не подходит - {i[0]}")
        except Exception as ex:
            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Пост не подходит - {i[0]}")

print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Начинаем постить")
threads = []
for ac in acc:
    thread = threading.Thread(target=start_acc_post, args=(ac,),daemon=True)  # каждый аккаунт будет работать в потоке
    threads.append(thread)
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Запуск потока - {thread}")
    thread.start()
    time.sleep(5)
    #print('Ожидание дочерних')
for thread in threads:
    thread.join()

# for url in urls:
#    for ac in acc:
#        try:
#            url_create = url[0].split('wall')[1]
#            user_id, post_id = url_create.split('_')
#            completion = openai.ChatCompletion.create(
#                model="gpt-3.5-turbo",
#                messages=[
#                    {"role": "user", "content": f"{ac[1]}. Прокомментируй запись - {url[1]}"}
#                ]
#            )  # обращение к ChatGTP
#            send_comment(ac[0], completion.choices[0].message.content, user_id, post_id, url[0])  # Оставляем комментарий
#        except Exception as ex:
#            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] f{ex}")
#    time.sleep(int(time_sleep) * 60)
#    with open('comments.txt', "w") as file: # Обновляем список комментариев
#        file.writelines("%s\n" % line for line in com)
