import cx_Oracle
import configparser
import os

os.environ["NLS_LANG"] = "AMERICAN_CIS.CL8ISO8859P5"

def getdbsettings(ini_path):
    if not os.path.exists(ini_path):
        print("No ini files found")
    else:
        config = configparser.ConfigParser()
        config.read(ini_path)
    # Читаем значения из конфиг. файла.
        db_user = config.get("ABS DB", "user")
        db_user_pwd = config.get("ABS DB", "pwd")
        db_host = config.get("ABS DB", "dbhost")
        db_service_name = config.get("ABS DB", "service_name")

    return (db_user, db_user_pwd, db_host, db_service_name)

db_user, db_user_pwd, db_host, db_service_name = getdbsettings("absgate.ini")

def set_connection():
    return  cx_Oracle.connect("{}/{}@{}/{}".format(db_user, db_user_pwd, db_host, db_service_name))

try:
    con = set_connection()
except:
    print('[ERROR] DB Connection ERROR!')

def execPLSQL(plsql):
    con.execute(plsql)

def close_con():
    con.close()
