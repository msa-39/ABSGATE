from json2html import json2html
import requests
import datetime
import random
import string

API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5OTU3MzMwMywiZXhwIjoxNjMxMTA5MzAzfQ.eyJ1c2VybmFtZSI6ImJhbmtfY2xpZW50IiwiY3VzX2FjdGlvbl9nZXRfYWxsIjowLCJjdXNfYWN0aW9uX2dldCI6MSwiY3VzX2FjdGlvbl9wb3N0IjowLCJjdXNfYWN0aW9uX3B1dCI6MCwiY3VzX2FjdGlvbl9kZWxldGUiOjAsImFjY19hY3Rpb25fZ2V0IjoxLCJhY2NfYWN0aW9uX3Bvc3QiOjAsImFjY19hY3Rpb25fcHV0IjowLCJhY2NfYWN0aW9uX2RlbGV0ZSI6MCwiZG9jX2FjdGlvbl9nZXQiOjEsImRvY19hY3Rpb25fcG9zdCI6MSwiZG9jX2FjdGlvbl9wdXQiOjEsImRvY19hY3Rpb25fZGVsZXRlIjoxfQ.KbGVnHNiMcgm6MjF6lNmqS6iGXQ8C46SBx-3eYxPwSELotPFlu2Hzc1j2Cx_hfyWPEDK54o9KIvuB_WUfPW2gg'
# Expire_AT: 2021-09-08 16:55:03

BASE_URL = 'https://192.168.60.50:5003/absapi/v1/doc'
#BASE_URL = 'https://192.168.60.46:5003/absapi/v1/doc'

f = open('rezult.html', 'w')
f.close()

def register_rur_doc(j_doc):
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

doks =[{"IDSMR": '',
        "DOC_SUMMA": '1',
        "PRIORYTY": '',
        "DOC_NUM": random.randint(1,100),
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '40914810000000000768',
        "CPAY_NAME": 'Sergey A. Moiseev',
        "CPAY_INN": '390501893960',
        "CPAY_KPP": '',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '',
        "CREC_CORACC": '',
        "CREC_ACC": '',
        "CREC_NAME": '',
        "CREC_INN": '',
        "CREC_KPP": '',
        "CPURP": 'Тестовый исходящий платеж СБП. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC.',
        "NAL_STATUS_P101": '',
        "NAL_KBK_P104": '',
        "NAL_OKATO_P105": '',
        "NAL_OSNOVANIE_P106": '',
        "NAL_PERIOD_P107": '',
        "NAL_DOCNUM_P108": '',
        "NAL_DOCDATE_P109": '',
        "NAL_DOCTYPE_P110": '',
        "UIN_P22": '',
        "CSIGN1_FIO": '',
        "CSIGN2_FIO": '',
        "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)),
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": '',
        "SBP_ID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 13))
        },
       {"IDSMR": '',
        "DOC_SUMMA": '3',
        "PRIORYTY": '',
        "DOC_NUM": random.randint(1,100),
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '30232810200000000056',
        "CPAY_NAME": 'АО КБ "ИС Банк"',
        "CPAY_INN": '',
        "CPAY_KPP": '',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '',
        "CREC_CORACC": '',
        "CREC_ACC": '40914810000000000768',
        "CREC_NAME": 'Моисеев Сергей Алексеевич',
        "CREC_INN": '',
        "CREC_KPP": '',
        "CPURP": 'Тестовый входящий платеж СБП. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC.',
        "NAL_STATUS_P101": '',
        "NAL_KBK_P104": '',
        "NAL_OKATO_P105": '',
        "NAL_OSNOVANIE_P106": '',
        "NAL_PERIOD_P107": '',
        "NAL_DOCNUM_P108": '',
        "NAL_DOCDATE_P109": '',
        "NAL_DOCTYPE_P110": '',
        "UIN_P22": '',
        "CSIGN1_FIO": '',
        "CSIGN2_FIO": '',
        "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)),
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": '',
        "SBP_ID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 13))
        }]
for doc in doks:
    print(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))

#    f = open('rezult.html', 'a')
#    f.write(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))
#    f.close()
