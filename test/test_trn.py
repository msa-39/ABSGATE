import json
from json2html import json2html
import requests
import random
import datetime

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

doks = docs =[{"IDSMR": '',
        "DOC_SUMMA": '111',
        "PRIORYTY": '5',
        "DOC_NUM": '13',
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '40914810000000000768',
        "CPAY_NAME": 'Sergey A. Moiseev',
        "CPAY_INN": '390501893960',
        "CPAY_KPP": '',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '044525593',
        "CREC_CORACC": '',
        "CREC_ACC": '40702810302890003761',
        "CREC_NAME": 'ООО "МОТОМАРКЕТ"',
        "CREC_INN": '5001128154',
        "CREC_KPP": '500101001',
        "CPURP": '[IDSMR = , счет ГО] Тестовый ВНЕШНИЙ платеж. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC  Без НДС.',
        "NAL_STATUS_P101": '',
        "NAL_KBK_P104": '',
        "NAL_OKATO_P105": '',
        "NAL_OSNOVANIE_P106": '',
        "NAL_PERIOD_P107": '',
        "NAL_DOCNUM_P108": '',
        "NAL_DOCDATE_P109": '',
        "NAL_DOCTYPE_P110": '',
        "UIN_P22": '',
        "CSIGN1_FIO": 'Sign #1 (Иванов И.И.)',
        "CSIGN2_FIO": 'Sign #2 (Петров П.П.)',
        "CID": '20200213',
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": ''
        },
        {"IDSMR": '2',
        "DOC_SUMMA": '222',
        "PRIORYTY": '5',
        "DOC_NUM": '14',
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '40702810000000000010',
        "CPAY_NAME": 'ПАО "г/к "Ялта-Интурист"',
        "CPAY_INN": '9103007928',
        "CPAY_KPP": '910301001',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '044525349',
        "CREC_CORACC": '',
        "CREC_ACC": '40702810600000006688',
        "CREC_NAME": 'Общество с ограниченной ответственностью "ФрутЛогистик"',
        "CREC_INN": '5030070438',
        "CREC_KPP": '503001001',
        "CPURP": '[IDSMR = 2, счет ГО] Тестовый ВНУТРЕННИЙ платеж. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC  Без НДС.',
        "NAL_STATUS_P101": '',
        "NAL_KBK_P104": '',
        "NAL_OKATO_P105": '',
        "NAL_OSNOVANIE_P106": '',
        "NAL_PERIOD_P107": '',
        "NAL_DOCNUM_P108": '',
        "NAL_DOCDATE_P109": '',
        "NAL_DOCTYPE_P110": '',
        "UIN_P22": '',
        "CSIGN1_FIO": 'Sign #1 (Иванов И.И.)',
        "CSIGN2_FIO": 'Sign #2 (Петров П.П.)',
        "CID": '20200214',
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": ''
        },
       {"IDSMR": '1',
        "DOC_SUMMA": '333',
        "PRIORYTY": '3',
        "DOC_NUM": '15',
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '3',
        "CPAY_ACC": '40702810600000006688',
        "CPAY_NAME": 'Общество с ограниченной ответственностью "ФрутЛогистик"',
        "CPAY_INN": '5030070438',
        "CPAY_KPP": '503001001',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '044525000',
        "CREC_CORACC": '',
        "CREC_ACC": '40601810245253000002',
        "CREC_NAME": 'ГБОУ Школа № 1246',
        "CREC_INN": '7718228237',
        "CREC_KPP": '771801001',
        "CPURP": '[IDSMR = 1, счет Филиала] Тестовый НАЛОГОВЫЙ платеж. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC  Без НДС.',
        "NAL_STATUS_P101": '24',
        "NAL_KBK_P104": '07500000000131131022',
        "NAL_OKATO_P105": '45311000',
        "NAL_OSNOVANIE_P106": '0',
        "NAL_PERIOD_P107": '0',
        "NAL_DOCNUM_P108": '0',
        "NAL_DOCDATE_P109": '0',
        "NAL_DOCTYPE_P110": '0',
        "UIN_P22": '0349208702002009900028144',
        "CSIGN1_FIO": 'Sign #1 (Иванов И.И.)',
        "CSIGN2_FIO": 'Sign #2 (Петров П.П.)',
        "CID": '20200215',
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": ''
        },
        {"IDSMR": '3',
        "DOC_SUMMA": '11111',
        "PRIORYTY": '5',
        "DOC_NUM": '131',
        "DOC_DATE": datetime.datetime.now().strftime("%Y-%m-%d"),
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '40702810000020222233',
        "CPAY_NAME": 'ООО "Эстис"',
        "CPAY_INN": '7805027791',
        "CPAY_KPP": '780501001',
        "CREC_BANK_NAME": '',
        "CREC_BIC": '044525593',
        "CREC_CORACC": '',
        "CREC_ACC": '40702810302890003761',
        "CREC_NAME": 'ООО "МОТОМАРКЕТ"',
        "CREC_INN": '5001128154',
        "CREC_KPP": '500101001',
        "CPURP": '[IDSMR = 3, счет Филиала] Тестовый ВНЕШНИЙ платеж. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC  Без НДС.',
        "NAL_STATUS_P101": '',
        "NAL_KBK_P104": '',
        "NAL_OKATO_P105": '',
        "NAL_OSNOVANIE_P106": '',
        "NAL_PERIOD_P107": '',
        "NAL_DOCNUM_P108": '',
        "NAL_DOCDATE_P109": '',
        "NAL_DOCTYPE_P110": '',
        "UIN_P22": '',
        "CSIGN1_FIO": 'Sign #1 (Иванов И.И.)',
        "CSIGN2_FIO": 'Sign #2 (Петров П.П.)',
        "CID": '202002131',
        "CIP": '113.113.113.113',
        "CMAC": '0A-00-27-00-00-19',
        "C20PURP": ''
        }]
for doc in doks:
    print(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))

#    f = open('rezult.html', 'a')
#    f.write(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))
#    f.close()
