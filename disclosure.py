# *****************************************************************************
#   Программа disclosure.py предназначена для поиска на сайте
# www.e-disclosure.ru новых отчетов по МСФО. Исходные данные хранятся в файле
# input.txt в формате:
# id;value
# где id - номер эмитента на сайте www.e-disclosure.ru;
#     value - номер последней ссылки на странице финансовой отчетности
#             эмитента.
#   Для запуска программы необходим Python 3.0 и библиотеки urllib3, certifi
#   При выполнении в командной строке:
#   python disclosure.py
#                    Copyright (c) 2019 Логинов М.Д.
#  Разработчик: Логинов М.Д.
#  Модифицирован: 24 июня 2021 г.
#
# ******************************************************************************

# -*- coding: utf-8 -*-
import os
import urllib3
import certifi


# ******************************************************************************
#         Функция получения куки от сервера
# ******************************************************************************
def get_cookie():
    url = 'https://www.e-disclosure.ru/portal/files.aspx?id=9&type=4'
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where(),
                               timeout=urllib3.Timeout(connect=1.0, read=2.0))
    headers1 = {'Cookie': '', 'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 ' +
                'Firefox/83.0'}
    resp = http.request('GET', url, headers=headers1, retries=False)
    return resp.getheaders()['Set-Cookie']


# ******************************************************************************
#         Функция получения данных из Интернета и их анализа
# ******************************************************************************
def read_new_data(id, cookies):
    url = 'https://www.e-disclosure.ru/portal/files.aspx?id=0&type=4'
    url1 = url.replace('0', id)
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where(),
                               timeout=urllib3.Timeout(connect=1.0, read=2.0))
    headers1 = {'Cookie': cookies, 'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 ' +
                'Firefox/83.0'}
    resp = http.request('GET', url1, headers=headers1, retries=False)
    response = resp.data.decode('utf-8')
    f = str(response).split('\\r')
    # Следующая строка необходима для отладки offline
    # f=open('temp.html','r',encoding='utf-8')
    for line in f:
        if line.count('Fileid') > 0:
            str1 = line.split('Fileid=')
            str2 = str1[1].split('"')
            str3 = str2[0]
            break
    # f.close()
    return str3


# ******************************************************************************
#                  Функция сохранения отчета на диск
# ******************************************************************************
def save_report(id, cookies):
    url = 'https://www.e-disclosure.ru/portal/FileLoad.ashx?Fileid=' + id
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                               ca_certs=certifi.where(),
                               timeout=urllib3.Timeout(connect=1.0, read=2.0))
    headers1 = {'Cookie': cookies, 'User-Agent':
                'Mozilla/5.0 (X11; Linux x86_64; rv:83.0) Gecko/20100101 ' +
                'Firefox/83.0'}
    resp = http.request('GET', url, headers=headers1, retries=False)
    f = open('tmp', 'wb')
    f.write(resp.data)
    f.close()
    filenName = resp.headers['Content-Disposition'].split('=')[1]
    os.rename('tmp', filenName)
    return 0


# ******************************************************************************
#                       Текст основной программы
# ******************************************************************************
print('START')
siteCookie = get_cookie()
f = open('input.txt', 'r')
for line in f:
    str1 = line.split(";")
    id = str1[0]
    value = str1[1]
    newData = read_new_data(id, siteCookie)
    if value[:-1] != newData:
        print(id)
        save_report(newData, siteCookie)
f.close()
print('STOP')
