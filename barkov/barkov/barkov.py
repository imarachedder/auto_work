import pandas as pd
from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
import datetime
import csv
from python3_anticaptcha import ImageToTextTask
from functools import reduce
import pathlib


def parseBarkov():
    apath = pathlib.Path().absolute()
    with open(rf'{apath}/barkov/barkov/settings.txt', 'r', encoding='utf8') as file:  # считываем настройки
        settings = file.read().split('\n')

    df = pd.read_excel(f'{apath}/barkov/barkov/settings.xlsx')
    text_excel = [list(i) for i in df.values]

    phone = settings[0]
    password = settings[1]
    print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Начинаем парсер")
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': os.getcwd()}
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://vk.barkov.net/auth.aspx')  # запускаем парсер
    time.sleep(3)  # vkuiInput__el

    inp = driver.find_elements(By.CLASS_NAME, 'vkuiInput__el')[0]
    inp.clear()
    inp.send_keys(phone)

    time.sleep(3)  # vkuiButton__content vkuiText vkuiText--sizeY-compact vkuiText--w-2

    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    # btn = driver.find_element(By.CLASS_NAME,
    #                           'vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse'.replace(
    #                               ' ', '.'))
    btn.click()
    time.sleep(2)

    inp = driver.find_elements(By.NAME, 'password')[0]
    inp.clear()
    inp.send_keys(password)

    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    # btn = driver.find_element(By.CLASS_NAME,
    #                           'vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse'.replace(
    #                               ' ', '.'))
    btn.click()

    time.sleep(30)

    captcha = driver.find_elements(By.CLASS_NAME, 'vkc__Captcha__image.vkc__Captcha__adaptive')
    if captcha:
        image_link = captcha[0].get_attribute('src')

        ANTICAPTCHA_KEY = "574ec2ee05624706c561a7852f6a4c3f"
        user_answer = ImageToTextTask.ImageToTextTask(anticaptcha_key=ANTICAPTCHA_KEY). \
            captcha_handler(captcha_link=image_link)
        print(user_answer)
        captcha = driver.find_element(By.CLASS_NAME, "vkc__TextField__input")
        captcha.send_keys(user_answer['solution']['text'])
        btn_captcha = driver.find_element(By.CLASS_NAME, 'vkuiButton__in')
        btn_captcha.click()

        time.sleep(3)

    result_dict = {}
    exist_urls = set()

    for text in text_excel:

        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Начала запроса - {text[1]}")

        driver.get('https://vk.barkov.net/newsfeed.aspx')
        time.sleep(1)

        inp = driver.find_elements(By.CLASS_NAME, 'form-control')[1]
        inp.clear()
        inp.send_keys(text[1])

        inp = driver.find_element(By.ID, 'startDate')
        inp.clear()
        inp.send_keys('.'.join(settings[2].split('.')[::-1]))

        inp = driver.find_element(By.ID, 'finalDate')
        inp.clear()
        inp.send_keys('.'.join(settings[3].split('.')[::-1]))
        time.sleep(3)

        btn = driver.find_element(By.ID, 'submitNewsFeed'.replace(' ', '.'))
        btn.click()
        time.sleep(5)
        continue_flag = False
        n = 0
        while True:
            try:
                btns = driver.find_elements(By.CLASS_NAME, 'btn btn-primary'.replace(' ', '.'))  # скачиваем файл
                if n == 10:
                    continue_flag = True
                    break
                if btns:
                    flag = False
                    for i in btns:
                        if i.text.strip() == 'Скачать CSV (для Excel)':
                            flag = True
                            i.click()
                            break
                    if flag:
                        break
                n += 1
                time.sleep(3)
            except Exception as ex:
                continue

        if continue_flag:
            continue

        time.sleep(5)

        name_excel = ''  # ищем название нужного файла
        for i in os.listdir('/barkov/barkov/'):
            if 'csv' in i:
                name_excel = i
                break

        print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Файл {name_excel} получен")

        time.sleep(5)

        urls = []
        with open(rf"{apath}/barkov/barkov/{name_excel}", encoding='utf-8') as r_file:  # считываем скаченный файл
            file_reader = csv.reader(r_file, delimiter=";")
            for row in list(file_reader)[1:]:
                try:
                    if row and row[0] not in exist_urls:
                        exist_urls.add(row[0])
                        urls.append(row)
                except Exception as ex:
                    pass

        if text[0] not in result_dict.keys():
            result_dict[text[0]] = urls
        else:
            result_dict[text[0]] += urls

        try:
            os.remove(name_excel)
        except Exception as ex:
            pass

    print(result_dict.items())
    for key, item in result_dict.items():
        if not os.path.exists("/barkov/barkov/Готовые файлы"):
            os.makedirs("/barkov/barkov/Готовые файлы")

        for i in item[:]:
            c = i
            for j in item[:]:
                if i[0] == j[0] and i != j:
                    item.remove(j)
            if any(x in i[5].lower() for x in
                   ['помощ', 'благотворитель', 'гуманитар', 'волонтер', 'школ', 'квартир', ' орви', 'вич', 'животны',
                    'стоматолог', 'сбор']):
                try:
                    item.remove(i)
                except:
                    pass
        new_item = sorted(item, key=lambda x: int(x[9]), reverse=True)
        new_item = new_item[:100]
        with open(rf"{apath}/Охваты/Готовые файлы/{key}.csv", mode="w", encoding='utf-8-sig') as w_file:
            file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
            file_writer.writerow(
                'ССЫЛКА НА ЗАПИСЬ;ССЫЛКА НА ЗАПИСЬ С УЧЁТОМ ВЛАДЕЛЬЦА;ВЛАДЕЛЕЦ СТЕНЫ;АВТОР ЗАПИСИ;ДАТА И ВРЕМЯ;ТЕКСТ ПОСТА;ЛАЙКОВ;РЕПОСТОВ;КОММЕНТАРИЕВ;ПРОСМОТРОВ;ССЫЛКА НА КОММЕНТАРИЙ;НАЗВАНИЕ АВТОРА;ПОДПИСЧИКОВ'.split(
                    ';'))
            for line in new_item:
                file_writer.writerow(line)

        with open(f"{apath}/barkov/barkov/просмотры.csv", "a", encoding="utf-8") as f:
            file_writer = csv.writer(f, delimiter=";", lineterminator="\r")
            file_writer.writerow("НАЗВАНИЕ ТОВАРА;ДАТА;ПРОСМОТРЫ")
            for i in result_dict:
                file_writer.writerow([i, datetime.date.today(), sum([int(x[9]) for x in result_dict[i]])])


if __name__ == '__main__':
    parseBarkov()
