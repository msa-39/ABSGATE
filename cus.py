# Микросервис API для работы с клиентами
# Sergey A. Moiseev     06.01.2021      v.1.1.1

from flask import Flask, jsonify, make_response, request, g
import absdb
from flask_httpauth import HTTPTokenAuth
import clients
import json
import configparser
import os
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'abs_api_cus.log')

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
#app.config['JSON_SORT_KEYS'] = True

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

@app.route('/absapi/v1/cus', methods=['GET'])
# Get short information about ALL Custimers, hwo has opened account

@auth.login_required
def GetCusAll():

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    inn = request.args.get('inn')
    inn = (inn or '')
    con = None

    if not(clients.chek_priv(g.token, 'cus_action_get_all')) and inn == '':
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_all'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_all'}), 403)

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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_all_cus_info(:inn)) from dual"

    try:
        cu.execute(plSQL, inn=inn)
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
@app.route('/absapi/v1/cus/<int:icusnum>', methods=['GET'])
# Get short information about Custimer by icusnum

@auth.login_required
def GetCusInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/fullinfo', methods=['GET'])
# Get FULL information about Custimer by icusnum

@auth.login_required
def GetCusFullInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_full_info(:icusnum, :status)) from dual"

    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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
@app.route('/absapi/v1/cus/<int:icusnum>/addresses', methods=['GET'])
# Get Addresses of Customer by icusnum

@auth.login_required
def GetCusAddressesInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_addresses_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/phones', methods=['GET'])
# Get information about Custimer phones numbers by icusnum

@auth.login_required
def GetCusPhonesInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_phones_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/docums', methods=['GET'])
# Get information about Custimer docums by icusnum

@auth.login_required
def GetCusDocimsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_docs_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/links', methods=['GET'])
# Get information about Custimer Links by icusnum

@auth.login_required
def GetCusLinksInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_links_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/accounts', methods=['GET'])
# Get information about Custimer Accounts by icusnum

@auth.login_required
def GetCusAccountsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_accounts_info(:icusnum, :status)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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
@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/credits', methods=['GET'])
# Get information about Custimer Credits by icusnum

@auth.login_required
def GetCusCreditsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_credits_info(:icusnum, :status)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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
@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/garants', methods=['GET'])
# Get information about Custimer Garants by icusnum

@auth.login_required
def GetCusGarantsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_garants_info(:icusnum, :status)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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
@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/depozits', methods=['GET'])
# Get information about Custimer Deposits by icusnum

@auth.login_required
def GetCusDepositsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_depozits_info(:icusnum, :status)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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
@app.route('/absapi/v1/cus/<int:icusnum>/rentdogs', methods=['GET'])
# Get information about Custimer Rent Contracts

@auth.login_required
def GetCusRentdogsInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_rentdogs_info(:icusnum)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum)
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
@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/cards', methods=['GET'])
# Get information about Custimer Cards

@auth.login_required
def GetCusCardssInfo(icusnum):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'cus_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - cus_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - cus_action_get'}), 403)

    res = None
    con = None
    status = request.args.get('status')
    status = (status or '1')
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
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_cus.get_cus_cards_info(:icusnum, :status)) from dual"
    try:
        cu.execute(plSQL, icusnum=icusnum, status=status)
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

#@app.route('/absapi/v1/cus_full/', methods=['GET'])
#@auth.login_required
# Get FULL information about ALL Custimers, hwo has opened account
#def GetCusFullAll():
#    return make_response(jsonify({'msg': '[Ok] GetCusFullAll'}), 200)

#@app.route('/absapi/v1/cus_full/<int:icusnum>', methods=['GET'])
#@auth.login_required
# Get FULL information about Custimer by icusnum
#def GetCusFullInfo(icusnum):
#    return make_response(jsonify({'msg': '[Ok] GetCusFullInfo CusNum = '+str(icusnum)}), 200)

########################################################################################################################

def geta_cus_service_settings(ini_path):

    if not os.path.exists(ini_path):
        print("[ERROR] No ini files found")
        app.logger.error('[ERROR] No ini files found!')
        exit()
    else:
        config = configparser.ConfigParser()
        config.read(ini_path)

    # Читаем значения из конфиг. файла.
        l_cus_ip = config.get("SERVECES SETTINGS", "cus_ip")
        l_cus_port = config.get("SERVECES SETTINGS", "cus_port")
        l_ssl_cerf_file = config.get("SERVECES SETTINGS", "ssl_cert_file")
        l_ssl_key_file = config.get("SERVECES SETTINGS", "ssl_key_file")

    return (l_cus_ip, l_cus_port, l_ssl_cerf_file, l_ssl_key_file)

########################################################################################################################

cus_service_ip, cus_service_port, ssl_cert, ssl_key = geta_cus_service_settings("absgate.ini")

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
            debug=True, host=cus_service_ip, port=cus_service_port)