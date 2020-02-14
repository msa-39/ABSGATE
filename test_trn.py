import json
#from json2html import json2html
import requests

API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU4MTY5MTc3MywiZXhwIjoxNjEzMjI3NzczfQ.eyJ1c2VybmFtZSI6ImJhbmtfY2xpZW50IiwiY3VzX2FjdGlvbl9yZWFkIjoxfQ.ZNeDHfLSoKW_TAg7w9jWEq7OgnPrIFRB670WX6gndwlieo0YBsQs0kkRBgMpYsTtV_FDZHh01bn8qEuyl1Hu0Q'
# Expire_AT: 2021-02-13 17:49:33

BASE_URL = 'https://localhost:5003/absapi/v1/doc'

def register_rur_doc(j_doc):
    url = BASE_URL
    headers = {"Authorization": "Bearer %s" % API_KEY,
               "Content-Type": "application/json",
               "Accept": "application/json",
               }

    try:
        res = requests.post(url, data=None, json=j_doc, headers=headers, verify=False)
        data = res.json()

#        print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
#        print(json.dumps(data))
        print(data)
 #       print(json2html.convert(json=data))

    except Exception as e:
        print("Exception (getfromapi):", e)
        pass

    return data

doc1 = {"IDSMR": '',
        "DOC_SUMMA": '100',
        "PRIORYTY": '5',
        "DOC_NUM": '13',
        "DOC_DATE": '2020-02-14',
        "VID_PLAT_CODE": '',
        "CPAY_ACC": '40914810400000000009',
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
        "CTRNPURP": 'Тестовый ВНЕШНИЙ платеж. Регистрация через пакет ISB_ABS_API_DOCS.REG_RUR_DOC  Без НДС.',
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
        }

def get_doc_info(doc_id):
    return None

register_rur_doc(doc1)