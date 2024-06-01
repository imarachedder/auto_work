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

def coverage_parse():
    apath = pathlib.Path().absolute()
    with open(rf'{apath}/barkov/barkov/settings.txt', 'r', encoding='utf8') as file:  # считываем настройки
        set = file.read().split('\n')

    phone = set[0]
    password = set[1]
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

    # btn = driver.find_element(By.CLASS_NAME,
    #                           "vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse".replace(
    #                               " ", '.'))

    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
    # btn = driver.find_element(By.CLASS_NAME, "vkuiSplitCol.vkuiSplitCol--viewWidth-none.vkuiInternalSplitCol--viewWidth-none.vkc__AuthRoot__col.vkc__AuthRoot__promoCol")
    btn.click()
    time.sleep(2)

    inp = driver.find_elements(By.NAME, 'password')[0]
    inp.clear()
    inp.send_keys(password)

    # btn = driver.find_element(By.CLASS_NAME,
    #                           "vkuiButton vkuiButton--sz-l vkuiButton--lvl-primary vkuiButton--clr-accent vkuiButton--aln-center vkuiButton--sizeY-compact vkuiButton--stretched vkuiTappable vkuiTappable--sizeX-regular vkuiTappable--hasHover vkuiTappable--hasActive vkuiTappable--mouse".replace(
    #                               ' ', '.'))
    btn = driver.find_element(By.XPATH, "//button[@type='submit']")
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
    for mf in os.listdir("coverage/Готовые файлы"):
        with open(f"{apath}/coverage/Готовые файлы/mf", encoding="utf-8") as f:
            reader_object = csv.reader(f, delimiter=";")
            urls = [row[0] for row in reader_object][1:]

            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Парс для постов - {mf}")

            driver.get('https://vk.barkov.net/wallposts.aspx')
            time.sleep(1)

            btn = driver.find_element(By.ID, 'usersTab2')
            btn.click()

            inp = driver.find_element(By.ID, 'startDate')
            inp.clear()
            inp.send_keys('.'.join(set[2].split('.')[::-1]))

            inp = driver.find_element(By.ID, 'finalDate')
            inp.clear()
            inp.send_keys('.'.join(set[3].split('.')[::-1]))
            time.sleep(3)

            inp = driver.find_element(By.ID, 'postsLinks')
            inp.clear()
            inp.send_keys("\n".join(urls))

            time.sleep(2)

            driver.find_element(By.ID, "submitWallPosts").click()

            time.sleep(5)
            continue_flag = False
            n = 0
            while True:
                try:
                    btns = driver.find_elements(By.CLASS_NAME, 'btn btn-primary'.replace(' ', '.'))  # скачиваем файл
                    if n == 999:
                        continue_flag = True
                        break
                    if btns:
                        flag = False
                        for i in btns:
                            if i.text.strip() == 'Скачать CSV (для Excel)':
                                flag = True
                                driver.execute_script("arguments[0].click();", i)
                                break
                        if flag:
                            break
                    n += 1
                    time.sleep(3)
                except Exception as ex:
                    print(ex)
                    continue

            if continue_flag:
                continue

            time.sleep(5)

            name_excel = ''  # ищем название нужного файла
            for i in os.listdir("/coverage/"):
                if 'csv' in i and "vk.barkov.net" in i:
                    name_excel = i
                    break

            print(f"[{datetime.datetime.now().strftime('%H-%M-%S')}] Файл {name_excel} получен")

            time.sleep(5)

            urls = []
            with open(f"{apath}/coverage/{name_excel}", encoding='utf-8') as r_file:  # считываем скаченный файл
                file_reader = csv.reader(r_file, delimiter=";")
                for row in list(file_reader)[1:]:
                    try:
                        if row:
                            urls.append(int(row[14]))
                    except Exception as ex:
                        pass

            if mf not in result_dict.keys():
                result_dict[mf] = sum(urls)

            try:
                os.remove(name_excel)
            except Exception as ex:
                pass

    name_file = f"{apath}/coverage/просмотры-{datetime.date.today()}.csv"
    is_create_row = False
    if not os.path.exists(name_file):
        is_create_row = True


    with open(name_file, mode="a", encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r")
        if is_create_row:
            file_writer.writerow(["ТОВАР", "Дата", "ПРОСМОТРЫ"])
        for key, item in result_dict.items():
            file_writer.writerow([key.replace("csv", ''), datetime.date.today(), item])



