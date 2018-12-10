import sqlite3
import configparser
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import time
from flask import g

ini_path='absgate.ini'

if not os.path.exists(ini_path):
    print("[ERROR] No ini files found")
    exit()
else:
    config = configparser.ConfigParser()
    config.read(ini_path)
    # Читаем значения из конфиг. файла.
    api_secret_key = config.get("API", "secret_key")

EXPIRES_IN_A_YEAR = 365 * 24 * 60 * 60
ts = Serializer(api_secret_key, expires_in = EXPIRES_IN_A_YEAR)

users = ['dosie', 'bank_client']
for user in users:
    token = ts.dumps({'username': user, 'cus_action_read': 1}).decode('utf-8')
    print('*** token for {}: {}\n Expire_AT: {}'.format(user, token, datetime.datetime.fromtimestamp((int(time.time()) + EXPIRES_IN_A_YEAR))))
    print(ts.loads(token))

#@staticmethod
#    def verify_auth_token(token):
#        s = Serializer(api_secret_key)
#        try:
#            data = s.loads(token)
#        except SignatureExpired:
#            return None # valid token, but expired
#        except BadSignature:
#            return None # invalid token
#        user = User.query.get(data['id'])
#        return user

def check_key(key):
    g.user = None
    try:
        data = ts.loads(key)
    except:  # noqa: E722
        return False
    if 'username' in data:
        g.user = data['username']
        return True
    return False


