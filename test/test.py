import requests

url = 'https://192.168.60.46:5003/absapi/v1/doc'
API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5OTU3MzMwMywiZXhwIjoxNjMxMTA5MzAzfQ.eyJ1c2VybmFtZSI6ImJhbmtfY2xpZW50IiwiY3VzX2FjdGlvbl9nZXRfYWxsIjowLCJjdXNfYWN0aW9uX2dldCI6MSwiY3VzX2FjdGlvbl9wb3N0IjowLCJjdXNfYWN0aW9uX3B1dCI6MCwiY3VzX2FjdGlvbl9kZWxldGUiOjAsImFjY19hY3Rpb25fZ2V0IjoxLCJhY2NfYWN0aW9uX3Bvc3QiOjAsImFjY19hY3Rpb25fcHV0IjowLCJhY2NfYWN0aW9uX2RlbGV0ZSI6MCwiZG9jX2FjdGlvbl9nZXQiOjEsImRvY19hY3Rpb25fcG9zdCI6MSwiZG9jX2FjdGlvbl9wdXQiOjEsImRvY19hY3Rpb25fZGVsZXRlIjoxfQ.KbGVnHNiMcgm6MjF6lNmqS6iGXQ8C46SBx-3eYxPwSELotPFlu2Hzc1j2Cx_hfyWPEDK54o9KIvuB_WUfPW2gg'

values = \
  {
  "IDSMR":"1",
  "DOC_SUMMA":1600000,
  "PRIORYTY":5,
  "DOC_NUM":62,
  "DOC_DATE":"2020-10-13",
  "VID_PLAT_CODE":"2",

  "CPAY_ACC":"30232810200000000056",
  "CPAY_NAME":"АО КБ \"ИС БАНК\"",
  "CPAY_INN":"7744001673",
  "CPAY_KPP":"",

  "CREC_BANK_NAME":"АО КБ \"ИС БАНК\"",
  "CREC_BIC":"044525349",
  "CREC_CORACC":"",
  "CREC_ACC":"60308810500000000278",
  "CREC_NAME":"Левина Надия Асымовна",
  "CREC_INN":"504702340489",
  "CREC_KPP":"",

  "CPURP":"Получение перевода по СБП",

  "NAL_STATUS_P101":"",
  "NAL_KBK_P104":"",
  "NAL_OKATO_P105":"",
  "NAL_OSNOVANIE_P106":"",
  "NAL_PERIOD_P107":"..",
  "NAL_DOCNUM_P108":"",
  "NAL_DOCDATE_P109":"",
  "NAL_DOCTYPE_P110":"",
  "UIN_P22":"",

  "CSIGN1_FIO":"",
  "CSIGN2_FIO":"",

  "CID":"132",
  "CIP":"",
  "CMAC":"",

  "C20PURP":""
  }
"""
  {
    "IDSMR": "1",
    "DOC_SUMMA": 100,
    "PRIORYTY": 5,
    "DOC_NUM": 13,
    "DOC_DATE": "2020-02-21",
    "VID_PLAT_CODE": "2",
    "CPAY_ACC": "40702810134000006455",
    "CPAY_NAME": "Общество с ограниченной ответственностью \"ФорЛэкс\"",
    "CPAY_INN": "6670462690",
    "CPAY_KPP": "668601001",
    "CREC_BANK_NAME": "``",
    "CREC_BIC": "046577001",
    "CREC_CORACC": "``",
    "CREC_ACC": "40101810500000010010",
    "CREC_NAME": "Управление федерального казначейства по Свердловской области (Межрайонная ИФНС России №32 по Свердловской области)",
    "CREC_INN": "6686000010",
    "CREC_KPP": "668601001",
    "CTRNPURP": "Налог на добавленную стоимость. НДС не облагается.",
    "NAL_STATUS_P101": "01",
    "NAL_KBK_P104": "18210301000012100110",
    "NAL_OKATO_P105": "65701000",
    "NAL_OSNOVANIE_P106": "ТП",
    "NAL_PERIOD_P107": "0",
    "NAL_DOCNUM_P108": "0",
    "NAL_DOCDATE_P109": "25.07.2019",
    "NAL_DOCTYPE_P110": "``",
    "UIN_P22": "0",
    "CSIGN1_FIO": "Sign1 (Иванов И.И.)",
    "CSIGN2_FIO": "Sign2 (Петров П.П.)",
    "CID": "1234567890",
    "CIP": "113.113.113.113",
    "CMAC": "0A-00-27-00-00-19"
  }
"""

headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json',
  'Authorization': 'Bearer %s' % API_KEY
}

#request = Request('https://192.168.60.46:5003/absapi/v1/doc', data=values, headers=headers)

res = requests.post(url,  data=None, json=values, headers=headers, verify=False)
data = res.json()
print(data)

#response_body = urlopen(request).read()
#print(response_body)