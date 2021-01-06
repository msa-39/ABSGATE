from json2html import json2html
import requests
import datetime
import random
import string

API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5OTU3MzMwMywiZXhwIjoxNjMxMTA5MzAzfQ.eyJ1c2VybmFtZSI6ImJhbmtfY2xpZW50IiwiY3VzX2FjdGlvbl9nZXRfYWxsIjowLCJjdXNfYWN0aW9uX2dldCI6MSwiY3VzX2FjdGlvbl9wb3N0IjowLCJjdXNfYWN0aW9uX3B1dCI6MCwiY3VzX2FjdGlvbl9kZWxldGUiOjAsImFjY19hY3Rpb25fZ2V0IjoxLCJhY2NfYWN0aW9uX3Bvc3QiOjAsImFjY19hY3Rpb25fcHV0IjowLCJhY2NfYWN0aW9uX2RlbGV0ZSI6MCwiZG9jX2FjdGlvbl9nZXQiOjEsImRvY19hY3Rpb25fcG9zdCI6MSwiZG9jX2FjdGlvbl9wdXQiOjEsImRvY19hY3Rpb25fZGVsZXRlIjoxfQ.KbGVnHNiMcgm6MjF6lNmqS6iGXQ8C46SBx-3eYxPwSELotPFlu2Hzc1j2Cx_hfyWPEDK54o9KIvuB_WUfPW2gg'
# Expire_AT: 2021-09-08 16:55:03

BASE_URL = 'https://192.168.60.50:5003/absapi/v1/doc/val/convert'
#BASE_URL = 'https://192.168.60.46:5003/absapi/v1/doc/val/convert'


def register_val_sell(j_doc):
    url = BASE_URL
    headers = {"Authorization": "Bearer %s" % API_KEY,
               "Content-Type": "application/json",
               "Accept": "application/json",
               }

    try:
        res = requests.post(url, data=None, json=j_doc, headers=headers, verify=False)
        data = res.json()

        print(data)

    except Exception as e:
        print("Exception (getfromapi):", e)
        pass

    return data

def get_doc_info(doc_id):
    url = BASE_URL+'/'+doc_id
    headers = {"Authorization": "Bearer %s" % API_KEY,
               "Content-Type": "application/json",
               "Accept": "application/json",
               }
    try:
        res = requests.get(url, headers=headers, verify=False)
        data = res.json()

        print(data)

    except Exception as e:
        print("Exception (getfromapi):", e)
        pass

    return data

doks =[
    {
    "IDSMR": '1',

    "DATE_DOC": datetime.datetime.now().strftime("%Y-%m-%d"),
    "NUM_DOC": random.randint(1,100),

    "CLN_BNK_NAME": 'АО КБ "ИС БАНК"',
    "CLN_NAME": 'Общество с ограниченной ответственностью "СИТИФРУТ"',
    "CLN_INN": '7710967437',
    "CLN_OKPO": '17980787',
    "CLN_ADDR": 'Российская Федерация, Нижегородская обл, г. Нижний Новгород',
    "CLN_EMPLOYEE_FIO": 'Моисеев С. А.',
    "CLN_EMPLOYEE_PHONES": '+7 (926) 3090367',

    "SALE_SUM": '35000',
    "SALE_CURRENCY":'USD',
    "SALE_ACCOUNT": '40702840400000005464',

    "CONVERT_RATE_KIND": '1',
    "CONVERT_RATE": '',

    "BUY_SUM": '25000',
    "BUY_CURRENCY": 'EUR',
    "BUY_ACCOUNT": '40702978000000005464',

    "EXPERIENCE_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
    "TRANSFER_DATE": '',
    "ADDED_COND": '',

    "VCSIGN1": 'Тестовая подпись1',
    "VCSIGN2": 'Тестовая подпись2',

    "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)),
    "CIP": '111.111.111.111',
    "CMAC": '0A-00-27-00-00-19'
    }]
for doc in doks:
    rez = register_val_sell(doc)
    print('The END.')
#    print(rez)

    # print(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))
