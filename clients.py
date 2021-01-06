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
    api_db_file = config.get("API DB", "db_file")

EXPIRES_IN_A_YEAR = 365 * 24 * 60 * 60
ts = Serializer(api_secret_key, expires_in = EXPIRES_IN_A_YEAR)

########################################################################################################################

def check_key(key):
    g.user = None

    try:
        data = ts.loads(key)
    except:
        return False

    if 'username' in data:
        g.user = data['username']
        g.token = key
        return True

    return False

#######################################################################################################################

def chek_priv(key, priv):
    g_user_name = g.user
    allow_priv = 0

    try:
        data = ts.loads(key)
    except:
        return False

    if 'username' in data:
        k_user_name = data['username']
    else:
        k_user_name = 'FALUE'

    if g_user_name != k_user_name:
        return False

    if priv in data:
        allow_priv = data[priv]

    if allow_priv == 1:
        return True

    return False
