# Микросервис API для работы со счетами
# Sergey A. Moiseev     06.01.2021      v.1.1.1

import datetime
from flask import Flask, jsonify, make_response, g, request
import json
import absdb
from flask_httpauth import HTTPTokenAuth
import clients
import logging
import configparser
import os

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'abs_api_acc.log')

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

auth = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    return clients.check_key(token)

@auth.error_handler
def unauthorized():
    app.logger.debug('<Resp: {} >'.format('[ERROR 403] - Unauthorized access'))
    return make_response(jsonify({'ERROR': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def bad_request(error):
    app.logger.debug('<Resp: {} >'.format('[ERROR 400] - Bad request'))
    return make_response(jsonify({'ERROR': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    app.logger.debug('<Resp: {} >'.format('[ERROR 404] - Not found'))
    return make_response(jsonify({'ERROR': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    app.logger.debug('<Resp: {} >'.format('[ERROR 500] - Internal error'))
    return make_response(jsonify({'ERROR': 'Internal error'}), 500)

@app.errorhandler(503)
def not_available(error):
    app.logger.debug('<Resp: {} >'.format('[ERROR 503] - Service Unavailable'))
    return make_response(jsonify({'ERROR': 'Service Unavailable'}), 503)


########################################################################################################################
@app.route('/absapi/v1/acc/<int:p_idsmr>/<string:p_cacccur>/<int:p_iaccacc>/info', methods=['GET'])
# Get information about Account

@auth.login_required
def GetAccInfo(p_idsmr, p_cacccur, p_iaccacc):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'acc_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - acc_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - acc_action_get'}), 403)

    caccacc = str(p_iaccacc)
    cacccur = p_cacccur
    cidsmr = str(p_idsmr)
    res = None
    con = None

    try:
        if ((len(caccacc) != 20) or (len(cacccur) != 3)):
            raise Exception("Bad request")

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return bad_request(400)

    try:
        con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        print('[ERROR] DB Connection ERROR!')
        return not_available(503)

    cu = con.cursor()
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_acc.get_acc_info(:p_caccacc, :p_cacccur, :p_idsmr)) from dual"
    try:
        cu.execute(plSQL, p_caccacc=str(p_iaccacc), p_cacccur=p_cacccur, p_idsmr=p_idsmr)
        res = cu.fetchall()

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        con.close()
        return internal_error(500)

    out_rez = make_response(jsonify(json.loads(res[0][0].read())), 200)
    con.close()

    app.logger.debug(out_rez)
    app.logger.debug(out_rez.json)

    return out_rez

########################################################################################################################
@app.route('/absapi/v1/acc/<int:p_idsmr>/<string:p_cacccur>/<int:p_iaccacc>/statement/<int:p_date_from>/<int:p_date_to>', methods=['GET'])
# Get Statement of Account from date_from to date_to

@auth.login_required
def GetAccStatement(p_idsmr, p_cacccur, p_iaccacc, p_date_from, p_date_to):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'acc_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - acc_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - acc_action_get'}), 403)

    res = None
    con = None

    caccacc = str(p_iaccacc)
    cacccur = p_cacccur
    cidsmr = str(p_idsmr)
    begin_date = str(p_date_from)
    end_date = str(p_date_to)

    try:
        date_time_begin = datetime.datetime.strptime(begin_date, '%Y%m%d')
        date_time_end = datetime.datetime.strptime(end_date, '%Y%m%d')
        if ((len(caccacc) != 20) or (len(cacccur) != 3) or (date_time_end < date_time_begin)):
            raise Exception("Bad request")
    except:
        return bad_request(400)

    try:
        con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        print('[ERROR] DB Connection ERROR!')
        app.logger.error('[ERROR] DB Connection ERROR!')
        return not_available(503)

    cu = con.cursor()

    try:
        res = cu.callfunc('isb_abs_api_acc.get_acc_statement_clob',
                          absdb.db.CLOB,
                          [caccacc, cacccur, cidsmr, begin_date, end_date])

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        con.close()
        return internal_error(500)

    out_rez = make_response(jsonify(json.loads(res.read())), 200)
    con.close()

    app.logger.debug(out_rez)
    app.logger.debug(out_rez.json)

    return out_rez

    #plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_acc.get_acc_statement(:p_caccacc, :p_cacccur, :p_idsmr, :p_date_from, :P_date_to)) from dual"
    #cu.execute(plSQL, p_caccacc=str(p_iaccacc), p_cacccur=p_cacccur, p_idsmr=p_idsmr, p_date_from=p_date_from, p_date_to=p_date_to)
    #res=cu.fetchall()
    #return make_response(jsonify(json.loads(res[0][0].read())), 200)

########################################################################################################################
"""

@app.route('/absapi/v1/acc/<int:iacccur>/<int:iaccacc>/balance', methods=['GET'])
# Get information about Account balance
def GetAccBalance(iacccur, iaccacc):
    return make_response("[Ok] GetAccBalance\n Acc = "+str(iaccacc), 200)

@app.route('/absapi/v1/acc/<int:iacccur>/<int:iaccacc>/gab', methods=['GET'])
# Get GAB for Account
def GetAccGab(iacccur, iaccacc):
    return make_response("[Ok] GetAccGab\n Acc = "+str(iaccacc), 200)

@app.route('/absapi/v1/acc', methods=['POST'])
# Open new Acount in REZERV status
def RezervNewAcc():
    try:
        req_json = json.loads(request.data)

        key = request.headers.get("Key")

        p_ext_account = req_json['p_ext_account']
        p_ext_cus_id = req_json['p_ext_cus_id']
        p_ext_cus_status = req_json['p_ext_cus_status']

        return make_response("Ok key = {}\n".format(key), 200)

    except:
        return make_response ("Error\n "
                              "request_data = {} \n "
                              "req_json = {} \n "
                              "p_ext_account = {} \n "
                              "p_ext_cus_id = {} \n "
                              "p_ext_cus_status = {} \n"
                              .format(request.data,
                                      req_json,
                                      p_ext_account,
                                      p_ext_cus_id,
                                      p_ext_cus_status), 400)

@app.route('/absapi/v1/acc/<int:iacccur>/<int:iaccacc>', methods=['PUT'])
# Chane Acount status from REZERV to OPEN
def ChangeAccStatus(iacccur, iaccacc):
    return make_response("[Ok] ChangeAccStatus\n Acc = "+str(iaccacc), 200)

"""
########################################################################################################################

def get_acc_service_settings(ini_path):

    if not os.path.exists(ini_path):
        print("[ERROR] No ini files found")
        exit()
    else:
        config = configparser.ConfigParser()
        config.read(ini_path)

    # Читаем значения из конфиг. файла.
        l_acc_ip = config.get("SERVECES SETTINGS", "acc_ip")
        l_acc_port = config.get("SERVECES SETTINGS", "acc_port")
        l_ssl_cerf_file = config.get("SERVECES SETTINGS", "ssl_cert_file")
        l_ssl_key_file = config.get("SERVECES SETTINGS", "ssl_key_file")

    return (l_acc_ip, l_acc_port, l_ssl_cerf_file, l_ssl_key_file)

########################################################################################################################

acc_service_ip, acc_service_port, ssl_cert, ssl_key = get_acc_service_settings("absgate.ini")

if __name__ == '__main__':
    app.logger.debug(
        "-------------------------------------------------------------------------------------------------------")
    app.logger.debug("Running: Machine Name - {}; User Name - {}; User Domain - {}".format(os.getenv("COMPUTERNAME"),
                                                                                           os.getenv("USERNAME"),
                                                                                           os.getenv("USERDOMAIN")))
    app.logger.debug("DB Connection: {}".format(absdb.dsn))

    try:
        testcon = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
    app.logger.debug(
        "DB Connection: {} DB Version - {} DB_Client Version - {}".format("Ok!", testcon.version, absdb.db.clientversion()))
    testcon.close()

    app.run(ssl_context=(ssl_cert, ssl_key),
            debug=True, host=acc_service_ip, port=acc_service_port)


