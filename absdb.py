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
        l_db_host = config.get("ABS DB", "dbhost")
        l_db_port = config.get("ABS DB", "dbport")
        l_db_service_name = config.get("ABS DB", "service_name")

        l_db_user = config.get("ABS DB", "user")
        l_db_user_pwd = config.get("ABS DB", "pwd")

        l_db_f1user = config.get("ABS DB", "f1user")
        l_db_f1user_pwd = config.get("ABS DB", "f1pwd")

        l_db_f2user = config.get("ABS DB", "f2user")
        l_db_f2user_pwd = config.get("ABS DB", "f2pwd")

    return (l_db_host, l_db_port, l_db_service_name, l_db_user, l_db_user_pwd, l_db_f1user, l_db_f1user_pwd, l_db_f2user, l_db_f2user_pwd)

db_host, db_port, db_service_name, db_user, db_user_pwd, db_f1user, db_f1user_pwd, db_f2user, db_f2user_pwd  = getdbsettings("absgate.ini")

dsn = db.makedsn(db_host, db_port, service_name=db_service_name)

def set_connection(p_db_user, p_db_user_pwd):
    l_con = db.connect(p_db_user, p_db_user_pwd, dsn)
    return l_con
