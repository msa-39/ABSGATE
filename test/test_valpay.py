from json2html import json2html
import requests
import datetime
import random
import string

API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU5OTU3MzMwMywiZXhwIjoxNjMxMTA5MzAzfQ.eyJ1c2VybmFtZSI6ImJhbmtfY2xpZW50IiwiY3VzX2FjdGlvbl9nZXRfYWxsIjowLCJjdXNfYWN0aW9uX2dldCI6MSwiY3VzX2FjdGlvbl9wb3N0IjowLCJjdXNfYWN0aW9uX3B1dCI6MCwiY3VzX2FjdGlvbl9kZWxldGUiOjAsImFjY19hY3Rpb25fZ2V0IjoxLCJhY2NfYWN0aW9uX3Bvc3QiOjAsImFjY19hY3Rpb25fcHV0IjowLCJhY2NfYWN0aW9uX2RlbGV0ZSI6MCwiZG9jX2FjdGlvbl9nZXQiOjEsImRvY19hY3Rpb25fcG9zdCI6MSwiZG9jX2FjdGlvbl9wdXQiOjEsImRvY19hY3Rpb25fZGVsZXRlIjoxfQ.KbGVnHNiMcgm6MjF6lNmqS6iGXQ8C46SBx-3eYxPwSELotPFlu2Hzc1j2Cx_hfyWPEDK54o9KIvuB_WUfPW2gg'
# Expire_AT: 2021-09-08 16:55:03

BASE_URL = 'https://192.168.60.50:5003/absapi/v1/doc/val/payment'
#BASE_URL = 'https://192.168.60.46:5003/absapi/v1/doc/val/payment'


def register_val_doc(j_doc):
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
    "AMOUNT": '100',
    "AMOUNT_CURRENCY": 'USD',
    "CLN_ACCOUNT": '40702840600000006412',
    "CLN_NAME": 'Company Fresh Limited Liability Company',
    "CLN_INN": '7708743119',
    "CLN_COUNTRY": 'RF',
    "CLN_CITY": '',
    "CLN_ADDR": '107045, Moscow, Lane Golovine Small, the house 5',
    "CLN_EMPLOYEE_PHONES": '',
    "CLN_EMPLOYEE_FIO": '',
    "CLN_BNK_BIC": '044525349',
    "CLN_BNK_BIC_TYPE": '',
    "INTERMED_BNK_BIC": '',
    "INTERMED_BNK_NAME": '',
    "INTERMED_BNK_CITY": '',
    "INTERMED_BNK_ADDR": '',
    "INTERMED_BNK_COUNTRY": '',
    "INTERMED_BNK_COUNTRY_CODE": '',
    "INTERMED_BNK_BIC_TYPE": '',
    "RCPT_BNK_BIC": 'PAHAAZ22XXX',
    "RCPT_BNK_NAME": 'PASHA BANK (HEAD OFFICE)',
    "RCPT_BNK_CITY": 'BAKU',
    "RCPT_BNK_ADDR": '1005 BAKU 15,Y.MAMMADALIYEV',
    "RCPT_BNK_COUNTRY": 'AZERBAIJAN',
    "RCPT_BNK_COUNTRY_CODE": '031',
    "RCPT_BNK_ACCOUNT": '',
    "RCPT_BNK_BIC_TYPE": 'SWIFT',
    "RCPT_NAME": 'VITAMIN VIO LLC',
    "RCPT_ACCOUNT": 'AZ36PAHA40170USDHC0100032156',
    "RCPT_CITY": 'SHAMKIR',
    "RCPT_ADDR": 'MAHMUDLU',
    "RCPT_COUNTRY": 'AZERBAIJAN',
    "RCPT_COUNTRY_CODE": '031',
    "EXPENSE_ACCOUNT": '40702810300000006412',
    "EXPENSE_TYPE": 'OUR',
    "PAYMENT_DETAILS": 'Payment for fruit under  contract 45 from 01.10.2019',
    "PAYMENT_ADDED_INFO": '',
    "CXR_ADDED_INFO": '',
    "CO_CODE": '11200',
    "DEAL_PASSPORT": '',
    "CONTRACT_NUM": '19100004/3175/0000/2/1',
    "GTD": '',
    "VCSIGN1": '',
    "VCSIGN2": '',
    "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k = 5)),
    "CIP": '',
    "CMAC": ''
    },
    {
    "IDSMR": '1',
    "DATE_DOC": datetime.datetime.now().strftime("%Y-%m-%d"),
    "NUM_DOC": random.randint(1, 1000),
    "AMOUNT": '1111',
    "AMOUNT_CURRENCY": 'USD',
    "CLN_ACCOUNT": '40702840600000006412',
    "CLN_NAME": 'Company Fresh Limited Liability Company',
    "CLN_INN": '7708743119',
    "CLN_COUNTRY": 'RF',
    "CLN_ADDR": '107045, Moscow, Lane Golovine Small, the house 5',
    "CLN_EMPLOYEE_PHONES": '+7(900)000-00-00',
    "CLN_EMPLOYEE_FIO": 'Иванов И. И.',
    "CLN_BNK_BIC": '044525349',
    "RCPT_BNK_BIC": 'PAHAAZ22XXX',
    "RCPT_BNK_NAME": 'PASHA BANK (HEAD OFFICE)',
    "RCPT_BNK_CITY": 'BAKU',
    "RCPT_BNK_ADDR": '1005 BAKU 15,Y.MAMMADALIYEV',
    "RCPT_BNK_COUNTRY": 'AZERBAIJAN',
    "RCPT_BNK_COUNTRY_CODE": '031',
    "RCPT_BNK_ACCOUNT": '',
    "RCPT_BNK_BIC_TYPE": 'SWIFT',
    "RCPT_NAME": 'VITAMIN VIO LLC',
    "RCPT_ACCOUNT": 'AZ36PAHA40170USDHC0100032156',
    "RCPT_CITY": 'SHAMKIR',
    "RCPT_ADDR": 'MAHMUDLU',
    "RCPT_COUNTRY": 'AZERBAIJAN',
    "RCPT_COUNTRY_CODE": '031',
    "EXPENSE_ACCOUNT": '40702810300000006412',
    "EXPENSE_TYPE": 'OUR',
    "PAYMENT_DETAILS": 'Payment for fruit under  contract 45 from 01.10.2019',
    "CO_CODE": '',
    "CONTRACT_NUM": '19100004/3175/0000/2/1',
    "VCSIGN1": 'ФИО Подпись1',
    "VCSIGN2": 'ФИО Подпись2',
    "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
    "CIP": '123.123.123.123',
    "CMAC": '0A-00-27-00-00-19'
    },
    {
    "IDSMR": '1',
     "DATE_DOC": datetime.datetime.now().strftime("%Y-%m-%d"),
    "NUM_DOC": random.randint(1, 1000),
    "AMOUNT": '222',
    "AMOUNT_CURRENCY": 'USD',
    "CLN_ACCOUNT": '40702840600000006412',
    "CLN_NAME": 'Company Fresh Limited Liability Company',
    "CLN_INN": '7708743119',
    "CLN_COUNTRY": 'RF',
    "CLN_ADDR": '107045, Moscow, Lane Golovine Small, the house 5',
    "CLN_EMPLOYEE_PHONES": '+7(900)000-00-00',
    "CLN_EMPLOYEE_FIO": 'Иванов И. И.',
    "CLN_BNK_BIC": '044525349',
    "RCPT_BNK_BIC": 'PAHAAZ22XXX',
    "RCPT_BNK_NAME": 'PASHA BANK (HEAD OFFICE)',
    "RCPT_BNK_CITY": 'BAKU',
    "RCPT_BNK_ADDR": '1005 BAKU 15,Y.MAMMADALIYEV',
    "RCPT_BNK_COUNTRY": 'AZERBAIJAN',
    "RCPT_BNK_COUNTRY_CODE": '031',
    "RCPT_BNK_ACCOUNT": '',
    "RCPT_BNK_BIC_TYPE": 'SWIFT',
    "RCPT_NAME": 'VITAMIN VIO LLC',
    "RCPT_ACCOUNT": 'AZ36PAHA40170USDHC0100032156',
    "RCPT_CITY": 'SHAMKIR',
    "RCPT_ADDR": 'MAHMUDLU',
    "RCPT_COUNTRY": 'AZERBAIJAN',
    "RCPT_COUNTRY_CODE": '031',
    "EXPENSE_ACCOUNT": '40702810300000006412',
    "EXPENSE_TYPE": 'OUR',
    "PAYMENT_DETAILS": 'Payment for fruit under  contract 45 from 01.10.2019',
    "CO_CODE": '',
    "CONTRACT_NUM": '',
    "VCSIGN1": 'ФИО Подпись1',
    "VCSIGN2": 'ФИО Подпись2',
    "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
    "CIP": '123.123.123.123',
    "CMAC": '0A-00-27-00-00-19'
    },
    {
    "IDSMR": '1',
    "DATE_DOC": datetime.datetime.now().strftime("%Y-%m-%d"),
    "NUM_DOC": random.randint(1, 100),
    "AMOUNT": '333',
    "AMOUNT_CURRENCY": 'USD',
    "CLN_ACCOUNT": '40702840600000006412',
    "CLN_NAME": 'Company Fresh Limited Liability Company',
    "CLN_INN": '7708743119',
    "CLN_COUNTRY": 'RUSSIAN FEDERATION',
    "CLN_CITY": 'MOSCOW',
    "CLN_ADDR": '107045, Moscow, Lane Golovine Small, the house 5',
    "CLN_EMPLOYEE_PHONES": '+7(000)000-00-00 ',
    "CLN_EMPLOYEE_FIO": 'Петров П.П.',
    "CLN_BNK_BIC": '044525349',
    "CLN_BNK_BIC_TYPE": 'BIC',
    "INTERMED_BNK_BIC": '',
    "INTERMED_BNK_NAME": 'BANK OF NEW YORK IRVT US 3N',
    "INTERMED_BNK_CITY": 'NEW YORK',
    "INTERMED_BNK_ADDR": '',
    "INTERMED_BNK_COUNTRY": 'UNITED STATES',
    "INTERMED_BNK_COUNTRY_CODE": '840',
    "INTERMED_BNK_BIC_TYPE": '',
    "RCPT_BNK_BIC": 'PAHAAZ22XXX',
    "RCPT_BNK_NAME": 'PASHA BANK (HEAD OFFICE)',
    "RCPT_BNK_CITY": 'BAKU',
    "RCPT_BNK_ADDR": '1005 BAKU 15,Y.MAMMADALIYEV',
    "RCPT_BNK_COUNTRY": 'AZERBAIJAN',
    "RCPT_BNK_COUNTRY_CODE": '031',
    "RCPT_BNK_ACCOUNT": '',
    "RCPT_BNK_BIC_TYPE": 'SWIFT',
    "RCPT_NAME": 'VITAMIN VIO LLC',
    "RCPT_ACCOUNT": 'AZ36PAHA40170USDHC0100032156',
    "RCPT_CITY": 'SHAMKIR',
    "RCPT_ADDR": 'MAHMUDLU',
    "RCPT_COUNTRY": 'AZERBAIJAN',
    "RCPT_COUNTRY_CODE": '031',
    "EXPENSE_ACCOUNT": '40702810300000006412',
    "EXPENSE_TYPE": 'OUR',
    "PAYMENT_DETAILS": 'Payment for fruit under  contract 45 from 01.10.2019',
    "PAYMENT_ADDED_INFO": '',
    "CXR_ADDED_INFO": '',
    "CO_CODE": '11200',
    "DEAL_PASSPORT": '',
    "CONTRACT_NUM": '19100004/3175/0000/2/1',
    "GTD": '',
    "VCSIGN1": '',
    "VCSIGN2": '',
    "CID": ''.join(random.choices(string.ascii_uppercase + string.digits, k=5)),
    "CIP": '',
    "CMAC": ''
    }]
for doc in doks:
    rez = register_val_doc(doc)
    print('The END')

    # print(json2html.convert(json=get_doc_info(register_rur_doc(doc)['DOCID'])))
