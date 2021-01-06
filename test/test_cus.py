import json
#from json2html import json2html
import requests

API_KEY = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU0NDA5ODM0MCwiZXhwIjoxNTc1NjM0MzQwfQ.eyJ1c2VybmFtZSI6ImRvc2llIn0.MTOjvlD5QRRk1ZRp9zzT0G0_G6KJqAsl8dnnJU38_Qn99ufFe92Bsz89iYudYtZzGUib_QMKnTV3QNa7Sahsyg'
BASE_URL = 'https://localhost:5002/absapi/v1/'

def getffullcusinfo():
    url = BASE_URL+'cus/222512'
    headers = {"Authorization": "Bearer %s" % API_KEY,
               "Content-Type": "application/json",
               "Accept": "application/json",
               }

    try:
        res = requests.get(url, headers=headers, verify=False)
        data = res.json()

        print(json.dumps(data, sort_keys=True, indent=4, ensure_ascii=False))
        print(json.dumps(data))
        print(data)
 #       print(json2html.convert(json=data))

    except Exception as e:
        print("Exception (getfromapi):", e)
        pass

    return data

getffullcusinfo()