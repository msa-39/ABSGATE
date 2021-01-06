import sqlite3
import configparser
import os
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import datetime
import time

ini_path='absgate.ini'

if not os.path.exists(ini_path):
    print("[ERROR] No ini files found")
    exit()
else:
    config = configparser.ConfigParser()
    config.read(ini_path)
    # Читаем значения из конфиг. файла.
    api_db_file = config.get("API DB", "db_file")
    api_secret_key = config.get("API", "secret_key")

api_db_connection = sqlite3.connect(api_db_file)
api_db_cursor = api_db_connection.cursor()

sql_q = "create table api_users( " \
      "                 _id                     INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL, " \
      "                 username                TEXT, " \
      "                 cus_action_get_all      INTEGER, " \
      "                 cus_action_get          INTEGER, " \
      "                 cus_action_post         INTEGER, " \
      "                 cus_action_put          INTEGER, " \
      "                 cus_action_delete       INTEGER, " \
      "                 acc_action_get          INTEGER, " \
      "                 acc_action_post         INTEGER, " \
      "                 acc_action_put          INTEGER, " \
      "                 acc_action_delete       INTEGER, " \
      "                 doc_action_get          INTEGER, " \
      "                 doc_action_post         INTEGER, " \
      "                 doc_action_put          INTEGER, " \
      "                 doc_action_delete       INTEGER, " \
      "                 cur_token               TEXT, " \
      "                 token_end_date          DATE " \
      "             )"
#print(sql_q)
api_db_cursor.execute(sql_q);

EXPIRES_IN_A_YEAR = 365 * 24 * 60 * 60
ts = Serializer(api_secret_key, expires_in = EXPIRES_IN_A_YEAR)

users = [(1, 'isbank',      1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, None),
         (2, 'dosie',       0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, None, None),
         (3, 'bank_client', 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, None, None)]

query = "insert into api_users values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

api_db_cursor.executemany(query, users)

tokens = [(ts.dumps({'username':'isbank',
                      'cus_action_get_all': 1,
                      'cus_action_get': 1,
                      'cus_action_post': 1,
                      'cus_action_put': 1,
                      'cus_action_delete': 1,
                      'acc_action_get': 1,
                      'acc_action_post': 1,
                      'acc_action_put': 1,
                      'acc_action_delete': 1,
                      'doc_action_get': 1,
                      'doc_action_post': 1,
                      'doc_action_put': 1,
                      'doc_action_delete': 1,
                     }).decode('utf-8'),
           datetime.datetime.fromtimestamp((int(time.time()) + EXPIRES_IN_A_YEAR)),
           1),
          (ts.dumps({'username': 'dosie',
                     'cus_action_get_all': 0,
                     'cus_action_get': 1,
                     'cus_action_post': 0,
                     'cus_action_put': 0,
                     'cus_action_delete': 0,
                     'acc_action_get': 1,
                     'acc_action_post': 0,
                     'acc_action_put': 0,
                     'acc_action_delete': 0,
                     'doc_action_get': 0,
                     'doc_action_post': 0,
                     'doc_action_put': 0,
                     'doc_action_delete': 0,
                     }).decode('utf-8'),
           datetime.datetime.fromtimestamp((int(time.time()) + EXPIRES_IN_A_YEAR)),
           2),
          (ts.dumps({'username': 'bank_client',
                     'cus_action_get_all': 0,
                     'cus_action_get': 1,
                     'cus_action_post': 0,
                     'cus_action_put': 0,
                     'cus_action_delete': 0,
                     'acc_action_get': 1,
                     'acc_action_post': 0,
                     'acc_action_put': 0,
                     'acc_action_delete': 0,
                     'doc_action_get': 1,
                     'doc_action_post': 1,
                     'doc_action_put': 1,
                     'doc_action_delete': 1,
                     }).decode('utf-8'),
           datetime.datetime.fromtimestamp((int(time.time()) + EXPIRES_IN_A_YEAR)),
           3)]

update_sql = "update api_users set cur_token = ?, token_end_date = ? where _id = ?"

api_db_cursor.executemany(update_sql, tokens)

api_db_connection.commit()
api_db_connection.close()
