# *****************************************************************************
#   Программа disclosure.py предназначена для поиска на сайте
# www.e-disclosure.ru новых отчетов по МСФО. Исходные данные хранятся в файле
# input.txt в формате:
# id;value
# где id - номер эмитента на сайте www.e-disclosure.ru;
#     value - номер последней ссылки на странице финансовой отчетности
#             эмитента.
#   Для запуска программы необходим Python 3.0
#   При выполнении в командной строке:
#   python disclosure.py
#                    Copyright (c) 2019 Логинов М.Д.
#  Разработчик: Логинов М.Д.
#  Модифицирован: 30 марта 2020 г.
#
# ******************************************************************************

# -*- coding: utf-8 -*-
import urllib.request
import os


# ******************************************************************************
#         Функция получения данных из Интернета и их анализа
# ******************************************************************************
def read_new_data(id):
    url = 'http://www.e-disclosure.ru/portal/files.aspx?id=0&type=4&attempt=1'
    url1 = url.replace('0', id)
    response = urllib.request.urlopen(url1).read()
    f = str(response).split('\\r')
    # Следующая строка необходима для отладки offline
    # f=open('temp.html','r',encoding='utf-8')
    for line in f:
        if line.count('Fileid') > 0:
            # print(line)
            str1 = line.split('Fileid=')
            str2 = str1[1].split('"')
            str3 = str2[0]
            break
    # f.close()
    return str3


# ******************************************************************************
#                  Функция сохранения отчета на диск
# ******************************************************************************
def save_report(id):
    url = 'http://www.e-disclosure.ru/portal/FileLoad.ashx?Fileid='
    tempFile, headers = urllib.request.urlretrieve(url+id, "tmp")
    for line in headers.values():
        if line.count('filename') > 0:
            print(line.split('=')[1].replace('"', ''))
            os.rename('tmp', line.split('=')[1].replace('"', ''))
    return 0


# ******************************************************************************
#                       Текст основной программы
# ******************************************************************************
print('START')
f = open('input.txt', 'r')
for line in f:
    str1 = line.split(";")
    id = str1[0]
    value = str1[1]
    newData = read_new_data(id)
    if value[:-1] != newData:
        print(id)
        save_report(newData)
f.close()
print('STOP')
