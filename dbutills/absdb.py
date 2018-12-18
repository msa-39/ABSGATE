import json

import cx_Oracle as db
import configparser
import os

os.environ["NLS_LANG"] = "AMERICAN_CIS.CL8ISO8859P5"

def getdbsettings(ini_path):
    if not os.path.exists(ini_path):
        print("[ERROR] No ini files found")
        exit()
    else:
        config = configparser.ConfigParser()
        config.read(ini_path)
    # Читаем значения из конфиг. файла.
        l_db_user = config.get("ABS DB", "user")
        l_db_user_pwd = config.get("ABS DB", "pwd")
        l_db_host = config.get("ABS DB", "dbhost")
        l_db_service_name = config.get("ABS DB", "service_name")

    return (l_db_user, l_db_user_pwd, l_db_host, l_db_service_name)

db_user, db_user_pwd, db_host, db_service_name = getdbsettings("absgate.ini")

def set_connection():
    return  db.connect("{}/{}@{}/{}".format(db_user, db_user_pwd, db_host, db_service_name))

#cu = con.cursor()
#cu.execute('SELECT idsmr, csmrname FROM smr_mf')
#result=cu.fetchall()
#print(json.dumps(result, ensure_ascii=False))

con = None

try:
    con = set_connection()
except:
    print('[ERROR] DB Connection ERROR!')


def execPLSQL(plsql):
    try:
        con = set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    cu.execute(plsql)
    result=cu.fetchall()
    return result

def closeCon():
    con.close()