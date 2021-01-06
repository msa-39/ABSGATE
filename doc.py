# Микросервис API для работы с проводками
# Sergey A. Moiseev     06.01.2021      v.1.1.1

from flask import Flask, jsonify, make_response, request, g
import json
import absdb
from flask_httpauth import HTTPTokenAuth
import clients
import re
import logging
import configparser
import os

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'abs_api_doc.log')

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

"""
try:
    con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
    f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
    f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
except:
    app.logger.error('[ERROR] DB Connection ERROR!')
#    return not_available(503)
"""

########################################################################################################################
@app.route('/absapi/v1/doc/<string:p_docid>', methods=['GET'])
# Get document (transaction) information

# Требуется авторизация
@auth.login_required
def GetTrnInfo(p_docid):

    app.logger.debug(request)

    if not(clients.chek_priv(g.token, 'doc_action_get')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_get'}), 403)

    try:
        l_doctype = re.match(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))', p_docid).group(0).upper()
        p_docid   =   re.sub(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))', '', p_docid)
        l_inum = int(re.match(r'\d+', p_docid).group(0))
        l_ianum = int(re.sub(r'\d+_', '', p_docid))

    except:
        return bad_request(400)

    try:
        con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
        cur = con.cursor()
    except:
        app.logger.error('[ERROR] DB Connection ERROR!')
        return not_available(503)

    plSQL = ''

    if re.fullmatch(r'TRN', l_doctype):
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_docs.get_trn_info(:p_inum, :p_ianum)) from dual"

    if re.fullmatch(r'DPD', l_doctype):
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_docs.get_dpd_info(:p_inum, :p_ianum)) from dual"

    if re.fullmatch(r'TRC', l_doctype):
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_docs.get_trc_info(:p_inum, :p_ianum)) from dual"

    if (len(plSQL) == 0):
        return bad_request(400)

    try:
        cur.execute(plSQL, p_inum=l_inum, p_ianum=l_ianum)
        res = cur.fetchall()
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    ret = jsonify(json.loads(res[0][0].read()))
    app.logger.debug(ret)
    app.logger.debug(ret.json)

    return make_response(ret, 200)

########################################################################################################################
@app.route('/absapi/v1/doc', methods=['GET'])
# Get document information. New function.

# Требуется авторизация
@auth.login_required
def GetDocInfo():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    l_doctype = None
    l_ext_doc_id = None
    l_inum = None
    l_ianum = None

    if not(clients.chek_priv(g.token, 'doc_action_get')):
        app.logger.error('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_get'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_get'}), 403)

    try:
        if 'DOCID' in in_json:
            DOCID   =   in_json['DOCID']    # Идентификатор документа в АБС. Формат "DoctypeInum_Ianum"
        else:
            DOCID = None
        if 'CID' in in_json:
            CID     =   in_json['CID']      # Идентификатор платежа в системе Банк-Клиент
        else:
            CID = None

    except:
        app.logger.error('Possible incorrect format of json body in GET request!')
        return bad_request(400)

    p_docid = str(DOCID)

#    app.logger.debug('p_docid = {}'.format(p_docid))

    if p_docid != 'None':
        try:
            l_doctype = re.match(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D)|(s|S)(w|W)(p|P))', p_docid).group(0).upper()
            p_docid   =   re.sub(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D)|(s|S)(w|W)(p|P))', '', p_docid)
            l_inum = int(re.match(r'\d+', p_docid).group(0))
            l_ianum = int(re.sub(r'\d+_', '', p_docid))
        except:
            app.logger.error('DOCID = {}. Bad DOCID!'.format(DOCID))
            return bad_request(400)

    l_ext_doc_id = str(CID)

    if l_ext_doc_id or l_doctype:
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_docs.get_doc_info(:p_ext_doc_id, :p_doctype, :p_inum, :p_ianum)) from dual"

        try:
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        except:
            app.logger.error('[ERROR] DB Connection ERROR!')
            return not_available(503)

        try:
            cur.execute(plSQL, p_ext_doc_id=l_ext_doc_id, p_doctype=l_doctype, p_inum=l_inum, p_ianum=l_ianum)
            res = cur.fetchall()
        except absdb.db.Error as exc:
            error, = exc.args
            app.logger.error("Oracle-Error-Code: {}".format(error.code))
            app.logger.error("Oracle-Error-Message: {}".format(error.message))
            return internal_error(500)

        ret = jsonify(json.loads(res[0][0].read()))
        app.logger.debug(ret)
        app.logger.debug(ret.json)
        if 'ERROR' in ret.json:
            app.logger.error('ABS returned ERROR - Bad request !!')
            return bad_request(400)
        else:
            return make_response(ret, 200)

    else:
        app.logger.error('DOCID and CID are NULL!')
        return bad_request(400)

########################################################################################################################
@app.route('/absapi/v1/doc', methods=['POST'])
# Register RUR PayMent

# Требуется авторизация
@auth.login_required
def RegRURPayment():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_post')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_post'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_post'}), 403)

    #print(json.dumps(in_json))
    #print(in_json)

    try:
# Платежная информация о документе
        IDSMR           =   in_json['IDSMR']                  # ID Банка (Филиала), где зарегистрирован документ
        DOC_SUMMA       =   in_json['DOC_SUMMA']              # Сумма документа (платежа) в КОПЕЙКАХ
        PRIORYTY        =   in_json['PRIORYTY']               # Очередность платежа
        DOC_NUM         =   in_json['DOC_NUM']                # Номер документа
        DOC_DATE        =   in_json['DOC_DATE']               # Дата документа в формате ГГГГ-ММ-ДД 00:00:00
        VID_PLAT_CODE   =   in_json['VID_PLAT_CODE']          # Код вида платежа / 0-Почтой; 1-Телеграфом; 2-Электронно; 3-Срочно /

# Плательщик
        CPAY_ACC        =   in_json['CPAY_ACC']               # Счет ПЛАТЕЛЬЩИКА
        CPAY_NAME       =   in_json['CPAY_NAME']              # Наименование ПЛАТЕЛЬЩИКА
        CPAY_INN        =   in_json['CPAY_INN']               # ИНН ПЛАТЕЛЬЩИКА
        CPAY_KPP        =   in_json['CPAY_KPP']               # КПП ПЛАТЕЛЬЩИКА

# Получатель
        CREC_BANK_NAME  =   in_json['CREC_BANK_NAME']         # Наименование банка ПОЛУЧАТЕЛЯ
        CREC_BIC        =   in_json['CREC_BIC']               # БИК банка ПОЛУЧАТЕЛЯ
        CREC_CORACC     =   in_json['CREC_CORACC']            # Корреспонденский счет банка ПОЛУЧАТЕЛЯ
        CREC_ACC        =   in_json['CREC_ACC']               # Счет ПОЛУЧАТЕЛЯ
        CREC_NAME       =   in_json['CREC_NAME']              # Наименование ПОЛУЧАТЕЛЯ
        CREC_INN        =   in_json['CREC_INN']               # ИНН ПОЛУЧАТЕЛЯ
        CREC_KPP        =   in_json['CREC_KPP']               # КПП ПОЛУЧАТЕЛЯ

# Назначение платежа
        CPURP           =   in_json['CPURP']                  # Назначение платежа

# Налоговая информация
        NAL_STATUS_P101     =   in_json['NAL_STATUS_P101']    # Статус составителя (платеж в бюджет поле 101)
        NAL_KBK_P104        =   in_json['NAL_KBK_P104']       # Код Бюджетной Классификации /КБК/ (платеж в бюджет поле 104)
        NAL_OKATO_P105      =   in_json['NAL_OKATO_P105']     # Код ОКАТО/ОКТМО (платеж в бюджет поле 105)
        NAL_OSNOVANIE_P106  =   in_json['NAL_OSNOVANIE_P106'] # Основание налогового платежа (платеж в бюджет поле 106)
        NAL_PERIOD_P107     =   in_json['NAL_PERIOD_P107']    # Налоговый период (платеж в бюджет поле 107)
        NAL_DOCNUM_P108     =   in_json['NAL_DOCNUM_P108']    # Номер налогового документа (платеж в бюджет поле 108)
        NAL_DOCDATE_P109    =   in_json['NAL_DOCDATE_P109']   # Дата налогового документа (платеж в бюджет поле 109)
        NAL_DOCTYPE_P110    =   in_json['NAL_DOCTYPE_P110']   # Тип налогового платежа (платеж в бюджет поле 110)
        UIN_P22             =   in_json['UIN_P22']            # УИН (платеж в бюджет поле Код22)

# ЭЦП
        CSIGN1_FIO      =   in_json['CSIGN1_FIO']             # ФИО (Подпись) первого лица
        CSIGN2_FIO      =   in_json['CSIGN2_FIO']             # ФИО (Подпись) второго лица

# Идентификаторы
        CID             =   in_json['CID']                    # Идентификатор платежа в системе Банк-Клиент
        CIP             =   in_json['CIP']                    # IP-адрес, с которого был отправлен документ
        CMAC            =   in_json['CMAC']                   # MAC-адрес, с которого был отправлен документ

        if 'SBP_ID' in in_json:
            SBP_ID      =   in_json['SBP_ID']                 # ID документа в системе СБП (НЕ ОБЯЗАТЕЛЬНЫЙ атрибут)
        else:
            SBP_ID      =   None

# С 2020 года новое поле "Код вида дохода", введенное указанием БР № 5286-У
        C20PURP         =   in_json['C20PURP']                # 5286-У код вида дохода

    except:
        app.logger.error('Possible incorrect format of json body in POST !')
        return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE     =   cur.var(int)                  #  Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    RETMSG      =   cur.var(absdb.db.STRING)      #  Строка с сообщением о результате
    DOCID       =   cur.var(absdb.db.STRING)      #  Идентификатор документа в формате "doctype_inum_ianum"

    try:
        cur.callproc('isb_abs_api_docs.REG_RUR_DOC', [
            IDSMR,
            DOC_SUMMA,
            PRIORYTY,
            DOC_NUM,
            DOC_DATE,
            VID_PLAT_CODE,
# Плательщик
            CPAY_ACC,
            CPAY_NAME,
            CPAY_INN,
            CPAY_KPP,
# Получатель
            CREC_BANK_NAME,
            CREC_BIC,
            CREC_CORACC,
            CREC_ACC,
            CREC_NAME,
            CREC_INN,
            CREC_KPP,
            CPURP,
# Налоговая информация
            NAL_STATUS_P101,
            NAL_KBK_P104,
            NAL_OKATO_P105,
            NAL_OSNOVANIE_P106,
            NAL_PERIOD_P107,
            NAL_DOCNUM_P108,
            NAL_DOCDATE_P109,
            NAL_DOCTYPE_P110,
            UIN_P22,

            CSIGN1_FIO,
            CSIGN2_FIO,

            CID,
            CIP,
            CMAC,
            C20PURP,
            SBP_ID,
# Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue()>0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 201)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 200)


########################################################################################################################
@app.route('/absapi/v1/doc', methods=['DELETE'])
# Delete RUR PayMent / Отзыв руюлевого документа

# Требуется авторизация
@auth.login_required
def DelRURPayment():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_delete')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_delete'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_delete'}), 403)

    try:
        if 'IDSMR' in in_json:
            IDSMR = in_json['IDSMR']                # ID Банка (Филиала), где зарегистрирован документ
        else:
            IDSMR = '1'

        if 'CID' in in_json:
            CID  = in_json['CID']                   # Внешний iD документа (Идентификатор платежа в системе Банк-Клиент)
        else:
            CID = None

        if 'CREASON' in in_json:
            CREASON = in_json['CREASON']            # Причина отзыва документа
        else:
            CREASON = None

# Идентификаторы
        if 'CIP' in in_json:
            CIP = in_json['CIP']                    # IP-адрес, с которого был отправлен отзыв
        else:
            CIP = None

        if 'CMAC' in in_json:
            CMAC = in_json['CMAC']                   # MAC-адрес, с которого был отправлен отзыв
        else:
            CMAC = None

        if 'SBP_ID' in in_json:
            SBP_ID = in_json['SBP_ID']               # ID документа в системе СБП (НЕ ОБЯЗАТЕЛЬНЫЙ атрибут)
        else:
            SBP_ID = None

    except:
       app.logger.error('Possible incorrect format of json body in DELETE request!')
       return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE     =   cur.var(int)                  #  Код результата выполнения процедуры (-1 - ERROR; 1 - Отозван)
    RETMSG      =   cur.var(absdb.db.STRING)      #  Строка с сообщением о результате

    try:
        cur.callproc('isb_abs_api_docs.DEL_RUR_DOC', [
            CID,
            CREASON,
            CIP,
            CMAC,
            SBP_ID,
            # Выходные параметры
            RESCODE,
            RETMSG
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue()>0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 202)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 500)

########################################################################################################################
@app.route('/absapi/v1/doc/val/payment', methods=['POST'])
# Register VAL Document

# Требуется авторизация
@auth.login_required
def RegVALPayment():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_post')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_post'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_post'}), 403)

    #print(json.dumps(in_json))
    #print(in_json)

    try:
        if 'IDSMR' in in_json:
            IDSMR                       = in_json['IDSMR']                  # ID Банка (Филиала), где зарегистрирован документ
        else:
            IDSMR = None
# Данные  документа
        if 'DATE_DOC' in in_json:
            DATE_DOC                    = in_json['DATE_DOC']               # Дата документа
        else:
            DATE_DOC = None
        if 'NUM_DOC' in in_json:
            NUM_DOC                     = in_json['NUM_DOC']                # Номер документа
        else:
            NUM_DOC = None
        if 'AMOUNT' in in_json:
            AMOUNT                      = in_json['AMOUNT']                 # Сумма перевода
        else:
            AMOUNT = None
        if 'AMOUNT_CURRENCY' in in_json:
            AMOUNT_CURRENCY             = in_json['AMOUNT_CURRENCY']        # Валюта платежа
        else:
            AMOUNT_CURRENCY = None
# Перевододатель
        if 'CLN_ACCOUNT' in in_json:
            CLN_ACCOUNT                 = in_json['CLN_ACCOUNT']            # Счет перевододателя
        else:
            CLN_ACCOUNT = None
        if 'CLN_NAME' in in_json:
            CLN_NAME                    = in_json['CLN_NAME']               # Наименование перевододателя
        else:
            CLN_NAME = None
        if 'CLN_INN' in in_json:
            CLN_INN                     = in_json['CLN_INN']                # ИНН перевододателя
        else:
            CLN_INN = None
        if 'CLN_COUNTRY' in in_json:
            CLN_COUNTRY                 = in_json['CLN_COUNTRY']            # Страна перевододателя
        else:
            CLN_COUNTRY = None
        if 'CLN_CITY' in in_json:
            CLN_CITY                    = in_json['CLN_CITY']               # Город перевододателя
        else:
            CLN_CITY = None
        if 'CLN_ADDR' in in_json:
            CLN_ADDR                    = in_json['CLN_ADDR']               # Адрес перевододателя
        else:
            CLN_ADDR = None
        if 'CLN_EMPLOYEE_PHONES' in in_json:
            CLN_EMPLOYEE_PHONES         = in_json['CLN_EMPLOYEE_PHONES']    # Контактные телефоны ответственного сотрудника перевододателя
        else:
            CLN_EMPLOYEE_PHONES = None
        if 'CLN_EMPLOYEE_FIO' in in_json:
            CLN_EMPLOYEE_FIO            = in_json['CLN_EMPLOYEE_FIO']       # Ф.И.О. ответственного сотрудника перевододателя
        else:
            CLN_EMPLOYEE_FIO = None
# Банк перевододателя
        if 'CLN_BNK_BIC' in in_json:
            CLN_BNK_BIC                 = in_json['CLN_BNK_BIC']            # Идентификационный код банка перевододателя
        else:
            CLN_BNK_BIC = None
        if 'CLN_BNK_BIC_TYPE' in in_json:
            CLN_BNK_BIC_TYPE            = in_json['CLN_BNK_BIC_TYPE']       # Тип идентификационного кода банка перевододателя (SWIFT/BIC)
        else:
            CLN_BNK_BIC_TYPE =None
# Банк-Посредник
        if 'INTERMED_BNK_BIC' in in_json:
            INTERMED_BNK_BIC            = in_json['INTERMED_BNK_BIC']       # Идентификационный код банка-посредника
        else:
            INTERMED_BNK_BIC = None
        if 'INTERMED_BNK_NAME' in in_json:
            INTERMED_BNK_NAME           = in_json['INTERMED_BNK_NAME']      # Наименование банка-посредника
        else:
            INTERMED_BNK_NAME = None
        if 'INTERMED_BNK_CITY' in in_json:
            INTERMED_BNK_CITY           = in_json['INTERMED_BNK_CITY']      # Город банка-посредника
        else:
            INTERMED_BNK_CITY = None
        if 'INTERMED_BNK_ADDR' in in_json:
            INTERMED_BNK_ADDR           = in_json['INTERMED_BNK_ADDR']      # Адрес банка-посредника
        else:
            INTERMED_BNK_ADDR = None
        if 'INTERMED_BNK_COUNTRY' in in_json:
            INTERMED_BNK_COUNTRY        = in_json['INTERMED_BNK_COUNTRY']   # Страна банка-посредника
        else:
            INTERMED_BNK_COUNTRY = None
        if 'INTERMED_BNK_COUNTRY_CODE' in in_json:
            INTERMED_BNK_COUNTRY_CODE   = in_json['INTERMED_BNK_COUNTRY_CODE']  # Код страны банка-посредника
        else:
            INTERMED_BNK_COUNTRY_CODE = None
        if 'INTERMED_BNK_BIC_TYPE' in in_json:
            INTERMED_BNK_BIC_TYPE       = in_json['INTERMED_BNK_BIC_TYPE']  # Тип идентификационного кода банка-посредника (SWIFT/BIC)
        else:
            INTERMED_BNK_BIC_TYPE = None
# Банк Бенефициара
        if 'RCPT_BNK_BIC' in in_json:
            RCPT_BNK_BIC                = in_json['RCPT_BNK_BIC']           # Идентификационный код банка бенефициара
        else:
            RCPT_BNK_BIC = None
        if 'RCPT_BNK_NAME' in in_json:
            RCPT_BNK_NAME               = in_json['RCPT_BNK_NAME']          # Наименование банка бенефициара
        else:
            RCPT_BNK_NAME = None
        if 'RCPT_BNK_CITY' in in_json:
            RCPT_BNK_CITY               = in_json['RCPT_BNK_CITY']          # Город банка бенефициара
        else:
            RCPT_BNK_CITY = None
        if 'RCPT_BNK_ADDR' in in_json:
            RCPT_BNK_ADDR               = in_json['RCPT_BNK_ADDR']          # Адрес банка бенефициара
        else:
            RCPT_BNK_ADDR = None
        if 'RCPT_BNK_COUNTRY' in in_json:
            RCPT_BNK_COUNTRY            = in_json['RCPT_BNK_COUNTRY']       # Страна банка бенефициара
        else:
            RCPT_BNK_COUNTRY = None
        if 'RCPT_BNK_COUNTRY_CODE' in in_json:
            RCPT_BNK_COUNTRY_CODE       = in_json['RCPT_BNK_COUNTRY_CODE']  # Код страны банка бенефициара
        else:
            RCPT_BNK_COUNTRY_CODE = None
        if 'RCPT_BNK_ACCOUNT' in in_json:
            RCPT_BNK_ACCOUNT            = in_json['RCPT_BNK_ACCOUNT']       # Номер счета банка бенефициара
        else:
            RCPT_BNK_ACCOUNT = None
        if 'RCPT_BNK_BIC_TYPE' in in_json:
            RCPT_BNK_BIC_TYPE           = in_json['RCPT_BNK_BIC_TYPE']      # Тип идентификационного кода банка бенефициара (SWIFT/BIC)
        else:
            RCPT_BNK_BIC_TYPE = None
# Бенефициар
        if 'RCPT_NAME' in in_json:
            RCPT_NAME                   = in_json['RCPT_NAME']              # Наименование бенефициара
        else:
            RCPT_NAME = None
        if 'RCPT_ACCOUNT' in in_json:
            RCPT_ACCOUNT                = in_json['RCPT_ACCOUNT']           # Номер счета бенефициара
        else:
            RCPT_ACCOUNT = None
        if 'RCPT_CITY' in in_json:
            RCPT_CITY                   = in_json['RCPT_CITY']              # Город бенефициара
        else:
            RCPT_CITY = None
        if 'RCPT_ADDR' in in_json:
            RCPT_ADDR                   = in_json['RCPT_ADDR']              # Адрес бенефициара
        else:
            RCPT_ADDR = None
        if 'RCPT_COUNTRY' in in_json:
            RCPT_COUNTRY                = in_json['RCPT_COUNTRY']           # Страна бенефициара
        else:
            RCPT_COUNTRY = None
        if 'RCPT_COUNTRY_CODE' in in_json:
            RCPT_COUNTRY_CODE           = in_json['RCPT_COUNTRY_CODE']      # Код страны бенефициара
        else:
            RCPT_COUNTRY_CODE = None
# Расходы по переводу
        if 'EXPENSE_ACCOUNT' in in_json:
            EXPENSE_ACCOUNT             = in_json['EXPENSE_ACCOUNT']        # Счет оплаты расходов по переводу
        else:
            EXPENSE_ACCOUNT = None
        if 'EXPENSE_TYPE' in in_json:
            EXPENSE_TYPE                = in_json['EXPENSE_TYPE']           # Способ оплаты расходов по переводу
        else:
            EXPENSE_TYPE = None
# Назначение платежа
        if 'PAYMENT_DETAILS' in in_json:
            PAYMENT_DETAILS             = in_json['PAYMENT_DETAILS']        # Назначение платежа
        else:
            PAYMENT_DETAILS = None
# Доп. инф-я
        if 'PAYMENT_ADDED_INFO' in in_json:
            PAYMENT_ADDED_INFO          = in_json['PAYMENT_ADDED_INFO']     # Дополнительная информация
        else:
            PAYMENT_ADDED_INFO = None
        if 'CXR_ADDED_INFO' in in_json:
            CXR_ADDED_INFO              = in_json['CXR_ADDED_INFO']         # Примечание
        else:
            CXR_ADDED_INFO = None
# Инф-я по валютному контролю
        if 'CO_CODE' in in_json:
            CO_CODE                     = in_json['CO_CODE']                # Код вида операции
        else:
            CO_CODE = None
        if 'DEAL_PASSPORT' in in_json:
            DEAL_PASSPORT               = in_json['DEAL_PASSPORT']          # Паспорт сделки
        else:
            DEAL_PASSPORT = None
        if 'CONTRACT_NUM' in in_json:
            CONTRACT_NUM                = in_json['CONTRACT_NUM']           # Уникальный номер контракта (кредитного договора)
        else:
            CONTRACT_NUM = None
        if 'GTD' in in_json:
            GTD                         = in_json['GTD']                    # Декларация на товары
        else:
            GTD = None
# Подписи
        if 'VCSIGN1' in in_json:
            VCSIGN1                     = in_json['VCSIGN1']                # Подпись первого лица
        else:
            VCSIGN1 = None
        if 'VCSIGN2' in in_json:
            VCSIGN2                     = in_json['VCSIGN2']                # Подпись второго лица
        else:
            VCSIGN2 = None
# Идентификация
        if 'CID' in in_json:
            CID                         = in_json['CID']                    # Внешний iD документа (Идентификатор платежа в системе Банк-Клиент)
        else:
            CID = None
        if 'CIP' in in_json:
            CIP                         = in_json['CIP']                    # IP-адрес, с которого был отправле документ
        else:
            CIP = None
        if 'CMAC' in in_json:
            CMAC                        = in_json['CMAC']                   # MAC-адрес, с которого был отправле документ
        else:
            CMAC = None
    except:
        app.logger.error('Possible incorrect format of json body in POST !')
        return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE     =   cur.var(int)                  #  Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    #ResCode.setvalue(0,-1)

    RETMSG      =   cur.var(absdb.db.STRING)      #  Строка с сообщением о результате
    #RetMsg.setvalue(0, '')

    DOCID       =   cur.var(absdb.db.STRING)      #  Идентификатор документа в формате "doctype_inum_ianum"
    #DOCID.setvalue(0, '')

    try:
        cur.callproc('isb_abs_api_docs.REG_VAL_DOC', [
            IDSMR,

            DATE_DOC,
            NUM_DOC,
            AMOUNT,
            AMOUNT_CURRENCY,

            CLN_ACCOUNT,
            CLN_NAME,
            CLN_INN,
            CLN_COUNTRY,
            CLN_CITY,
            CLN_ADDR,
            CLN_EMPLOYEE_PHONES,
            CLN_EMPLOYEE_FIO,

            CLN_BNK_BIC,
            CLN_BNK_BIC_TYPE,

            INTERMED_BNK_BIC,
            INTERMED_BNK_NAME,
            INTERMED_BNK_CITY,
            INTERMED_BNK_ADDR,
            INTERMED_BNK_COUNTRY,
            INTERMED_BNK_COUNTRY_CODE,
            INTERMED_BNK_BIC_TYPE,

            RCPT_BNK_BIC,
            RCPT_BNK_NAME,
            RCPT_BNK_CITY,
            RCPT_BNK_ADDR,
            RCPT_BNK_COUNTRY,
            RCPT_BNK_COUNTRY_CODE,
            RCPT_BNK_ACCOUNT,
            RCPT_BNK_BIC_TYPE,

            RCPT_NAME,
            RCPT_ACCOUNT,
            RCPT_CITY,
            RCPT_ADDR,
            RCPT_COUNTRY,
            RCPT_COUNTRY_CODE,

            EXPENSE_ACCOUNT,
            EXPENSE_TYPE,

            PAYMENT_DETAILS,

            PAYMENT_ADDED_INFO,
            CXR_ADDED_INFO,

            CO_CODE,
            DEAL_PASSPORT,
            CONTRACT_NUM,
            GTD,

            VCSIGN1,
            VCSIGN2,

            CID,
            CIP,
            CMAC,
    # Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue()>0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 201)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 200)

########################################################################################################################

@app.route('/absapi/v1/doc/val/sell', methods=['POST'])
# Register VAL Document Sell

# Требуется авторизация
@auth.login_required
def RegVALSell():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_post')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_post'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_post'}), 403)

    try:
        if 'IDSMR' in in_json:
            IDSMR                       = in_json['IDSMR']                  # ID Банка (Филиала), где зарегистрирован документ
        else:
            IDSMR = None
# Данные  документа
        if 'DATE_DOC' in in_json:
            DATE_DOC                    = in_json['DATE_DOC']               # Дата документа
        else:
            DATE_DOC = None
        if 'NUM_DOC' in in_json:
            NUM_DOC                     = in_json['NUM_DOC']                # Номер документа
        else:
            NUM_DOC = None
# Клиент
        if 'CLN_BNK_NAME' in in_json:
            CLN_BNK_NAME                = in_json['CLN_BNK_NAME']
        else:
            CLN_BNK_NAME = None
        if 'CLN_NAME' in in_json:
            CLN_NAME                    = in_json['CLN_NAME']
        else:
            CLN_NAME    = None
        if 'CLN_INN' in in_json:
            CLN_INN                     = in_json['CLN_INN']
        else:
            CLN_INN = None
        if 'CLN_OKPO' in in_json:
            CLN_OKPO                    = in_json['CLN_OKPO']
        else:
            CLN_OKPO    = None
        if 'CLN_ADDR' in in_json:
            CLN_ADDR                    = in_json['CLN_ADDR']
        else:
            CLN_ADDR    = None
        if 'CLN_EMPLOYEE_FIO' in in_json:
            CLN_EMPLOYEE_FIO            = in_json['CLN_EMPLOYEE_FIO']
        else:
            CLN_EMPLOYEE_FIO    = None
        if 'CLN_EMPLOYEE_PHONES' in in_json:
            CLN_EMPLOYEE_PHONES         = in_json['CLN_EMPLOYEE_PHONES']
        else:
            CLN_EMPLOYEE_PHONES = None
# Списание
        if 'SALE_SUM' in in_json:
            SALE_SUM                    = in_json['SALE_SUM']
        else:
            SALE_SUM    = None
        if 'SALE_CURRENCY' in in_json:
            SALE_CURRENCY               = in_json['SALE_CURRENCY']
        else:
            SALE_CURRENCY   = None
        if 'SALE_ACCOUNT' in in_json:
            SALE_ACCOUNT                = in_json['SALE_ACCOUNT']
        else:
            SALE_ACCOUNT    = None
        if 'SALE_RATE_KIND' in in_json:
            SALE_RATE_KIND              = in_json['SALE_RATE_KIND']
        else:
            SALE_RATE_KIND  = None
        if 'SALE_RATE' in in_json:
            SALE_RATE                   = in_json['SALE_RATE']
        else:
            SALE_RATE   = None
# Зачисление
        if 'RECEIVED_SUM' in in_json:
            RECEIVED_SUM                = in_json['RECEIVED_SUM']
        else:
            RECEIVED_SUM    = None
        if 'RECEIVED_ACCOUNT' in in_json:
            RECEIVED_ACCOUNT            = in_json['RECEIVED_ACCOUNT']
        else:
            RECEIVED_ACCOUNT    = None
        if 'RECEIVED_BNK_BIC' in in_json:
            RECEIVED_BNK_BIC            = in_json['RECEIVED_BNK_BIC']
        else:
            RECEIVED_BNK_BIC    = None
        if 'RECEIVED_BNK_ACCOUNT' in in_json:
            RECEIVED_BNK_ACCOUNT        = in_json['RECEIVED_BNK_ACCOUNT']
        else:
            RECEIVED_BNK_ACCOUNT    = None
        if 'RECEIVED_BNK_NAME' in in_json:
            RECEIVED_BNK_NAME           = in_json['RECEIVED_BNK_NAME']
        else:
            RECEIVED_BNK_NAME   = None
# Комиссия
        if 'COMMISSION_ACCOUNT' in in_json:
            COMMISSION_ACCOUNT          = in_json['COMMISSION_ACCOUNT']
        else:
            COMMISSION_ACCOUNT  = None
        if 'COMMISSION_KIND' in in_json:
            COMMISSION_KIND             = in_json['COMMISSION_KIND']
        else:
            COMMISSION_KIND = None
        if 'COMMISSION_SUM' in in_json:
            COMMISSION_SUM              = in_json['COMMISSION_SUM']
        else:
            COMMISSION_SUM  = None
        if 'COMMISSION_CURRENCY' in in_json:
            COMMISSION_CURRENCY         = in_json['COMMISSION_CURRENCY']
        else:
            COMMISSION_CURRENCY = None
# Дополнительно
        if 'EXPERIENCE_DATE' in in_json:
            EXPERIENCE_DATE             = in_json['EXPERIENCE_DATE']
        else:
            EXPERIENCE_DATE = None
        if 'ADDED_COND' in in_json:
            ADDED_COND                  = in_json['ADDED_COND']
        else:
            ADDED_COND  = None
# Подписи
        if 'VCSIGN1' in in_json:
            VCSIGN1 = in_json['VCSIGN1']  # Подпись первого лица
        else:
            VCSIGN1 = None
        if 'VCSIGN2' in in_json:
            VCSIGN2 = in_json['VCSIGN2']  # Подпись второго лица
        else:
            VCSIGN2 = None
# Идентификация
        if 'CID' in in_json:
            CID = in_json['CID']  # Внешний iD документа (Идентификатор платежа в системе Банк-Клиент)
        else:
            CID = None
        if 'CIP' in in_json:
            CIP = in_json['CIP']  # IP-адрес, с которого был отправле документ
        else:
            CIP = None
        if 'CMAC' in in_json:
            CMAC = in_json['CMAC']  # MAC-адрес, с которого был отправле документ
        else:
            CMAC = None
    except:
     app.logger.error('Possible incorrect format of json body in POST !')
     return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE = cur.var(int)  # Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    RETMSG = cur.var(absdb.db.STRING)  # Строка с сообщением о результате
    DOCID = cur.var(absdb.db.STRING)  # Идентификатор документа в формате "doctype_inum_ianum"

    try:
        cur.callproc('isb_abs_api_docs.REG_VAL_SELL', [
            IDSMR,
        # Данные  документа
            DATE_DOC,
            NUM_DOC,
        # Клиент
            CLN_BNK_NAME,
            CLN_NAME,
            CLN_INN,
            CLN_OKPO,
            CLN_ADDR,
            CLN_EMPLOYEE_FIO,
            CLN_EMPLOYEE_PHONES,
        # Списание валюты
            SALE_SUM,
            SALE_CURRENCY,
            SALE_ACCOUNT,
            SALE_RATE_KIND,
            SALE_RATE,
        # Зачисление рублей
            RECEIVED_SUM,
            RECEIVED_ACCOUNT,
            RECEIVED_BNK_BIC,
            RECEIVED_BNK_ACCOUNT,
            RECEIVED_BNK_NAME,
        # Комиссия
            COMMISSION_ACCOUNT,
            COMMISSION_KIND,
            COMMISSION_SUM,
            COMMISSION_CURRENCY,
        # Дополнительно
            EXPERIENCE_DATE,
            ADDED_COND,
        # Подписи
            VCSIGN1,
            VCSIGN2,
        # Идентификация
            CID,
            CIP,
            CMAC,
        # Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue() > 0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 201)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 200)

########################################################################################################################

@app.route('/absapi/v1/doc/val/buy', methods=['POST'])
# Register VAL Document Buy

# Требуется авторизация
@auth.login_required
def RegVALBuy():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_post')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_post'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_post'}), 403)

    try:
        if 'IDSMR' in in_json:
            IDSMR                       = in_json['IDSMR']                  # ID Банка (Филиала), где зарегистрирован документ
        else:
            IDSMR = None
# Данные  документа
        if 'DATE_DOC' in in_json:
            DATE_DOC                    = in_json['DATE_DOC']               # Дата документа
        else:
            DATE_DOC = None
        if 'NUM_DOC' in in_json:
            NUM_DOC                     = in_json['NUM_DOC']                # Номер документа
        else:
            NUM_DOC = None
# Клиент
        if 'CLN_BNK_NAME' in in_json:
            CLN_BNK_NAME                = in_json['CLN_BNK_NAME']
        else:
            CLN_BNK_NAME = None
        if 'CLN_NAME' in in_json:
            CLN_NAME                    = in_json['CLN_NAME']
        else:
            CLN_NAME    = None
        if 'CLN_INN' in in_json:
            CLN_INN                     = in_json['CLN_INN']
        else:
            CLN_INN = None
        if 'CLN_OKPO' in in_json:
            CLN_OKPO                    = in_json['CLN_OKPO']
        else:
            CLN_OKPO    = None
        if 'CLN_ADDR' in in_json:
            CLN_ADDR                    = in_json['CLN_ADDR']
        else:
            CLN_ADDR    = None
        if 'CLN_EMPLOYEE_FIO' in in_json:
            CLN_EMPLOYEE_FIO            = in_json['CLN_EMPLOYEE_FIO']
        else:
            CLN_EMPLOYEE_FIO    = None
        if 'CLN_EMPLOYEE_PHONES' in in_json:
            CLN_EMPLOYEE_PHONES         = in_json['CLN_EMPLOYEE_PHONES']
        else:
            CLN_EMPLOYEE_PHONES = None
# Зачисление валюты
        if 'BUY_SUM' in in_json:
            BUY_SUM = in_json['BUY_SUM']
        else:
            BUY_SUM = None
        if 'BUY_CURRENCY' in in_json:
            BUY_CURRENCY = in_json['BUY_CURRENCY']
        else:
            BUY_CURRENCY = None
        if 'BUY_ACCOUNT' in in_json:
            BUY_ACCOUNT = in_json['BUY_ACCOUNT']
        else:
            BUY_ACCOUNT = None
        if 'BUY_RATE_KIND' in in_json:
            BUY_RATE_KIND = in_json['BUY_RATE_KIND']
        else:
            BUY_RATE_KIND = None
        if 'BUY_RATE' in in_json:
            BUY_RATE = in_json['BUY_RATE']
        else:
            BUY_RATE = None
# Списание рублей
        if 'SALE_SUM' in in_json:
            SALE_SUM = in_json['SALE_SUM']
        else:
            SALE_SUM = None
        if 'SALE_ACCOUNT' in in_json:
            SALE_ACCOUNT = in_json['SALE_ACCOUNT']
        else:
            SALE_ACCOUNT = None
# Комиссия
        if 'COMMISSION_ACCOUNT' in in_json:
            COMMISSION_ACCOUNT = in_json['COMMISSION_ACCOUNT']
        else:
            COMMISSION_ACCOUNT = None
        if 'COMMISSION_KIND' in in_json:
            COMMISSION_KIND = in_json['COMMISSION_KIND']
        else:
            COMMISSION_KIND = None
        if 'COMMISSION_SUM' in in_json:
            COMMISSION_SUM = in_json['COMMISSION_SUM']
        else:
            COMMISSION_SUM = None
        if 'COMMISSION_CURRENCY' in in_json:
            COMMISSION_CURRENCY = in_json['COMMISSION_CURRENCY']
        else:
             COMMISSION_CURRENCY = None
# Дополнительно
        if 'EXPERIENCE_DATE' in in_json:
            EXPERIENCE_DATE = in_json['EXPERIENCE_DATE']
        else:
            EXPERIENCE_DATE = None
        if 'ADDED_COND' in in_json:
            ADDED_COND = in_json['ADDED_COND']
        else:
            ADDED_COND = None
# Подписи
        if 'VCSIGN1' in in_json:
            VCSIGN1 = in_json['VCSIGN1']  # Подпись первого лица
        else:
            VCSIGN1 = None
        if 'VCSIGN2' in in_json:
            VCSIGN2 = in_json['VCSIGN2']  # Подпись второго лица
        else:
            VCSIGN2 = None
# Идентификация
        if 'CID' in in_json:
            CID = in_json['CID']  # Внешний iD документа (Идентификатор платежа в системе Банк-Клиент)
        else:
            CID = None
        if 'CIP' in in_json:
            CIP = in_json['CIP']  # IP-адрес, с которого был отправле документ
        else:
            CIP = None
        if 'CMAC' in in_json:
            CMAC = in_json['CMAC']  # MAC-адрес, с которого был отправле документ
        else:
            CMAC = None
    except:
     app.logger.error('Possible incorrect format of json body in POST !')
     return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE = cur.var(int)  # Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    RETMSG = cur.var(absdb.db.STRING)  # Строка с сообщением о результате
    DOCID = cur.var(absdb.db.STRING)  # Идентификатор документа в формате "doctype_inum_ianum"

    try:
        cur.callproc('isb_abs_api_docs.REG_VAL_BUY', [
            IDSMR,
        # Данные  документа
            DATE_DOC,
            NUM_DOC,
        # Клиент
            CLN_BNK_NAME,
            CLN_NAME,
            CLN_INN,
            CLN_OKPO,
            CLN_ADDR,
            CLN_EMPLOYEE_FIO,
            CLN_EMPLOYEE_PHONES,
        # Зачисление валюты
            BUY_SUM,
            BUY_CURRENCY,
            BUY_ACCOUNT,
        # Курс покупки
            BUY_RATE_KIND,
            BUY_RATE,
        # Списание рублей
            SALE_SUM,
            SALE_ACCOUNT,
        # Комиссия
            COMMISSION_ACCOUNT,
            COMMISSION_KIND,
            COMMISSION_SUM,
            COMMISSION_CURRENCY,
        # Дополнительно
            EXPERIENCE_DATE,
            ADDED_COND,
        # Подписи
            VCSIGN1,
            VCSIGN2,
        # Идентификация
            CID,
            CIP,
            CMAC,
        # Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue() > 0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 201)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 200)

########################################################################################################################

@app.route('/absapi/v1/doc/val/convert', methods=['POST'])
# Register VAL Document Buy

# Требуется авторизация
@auth.login_required
def RegVALConvert():

    app.logger.debug(request)
    in_json = request.json
    app.logger.debug(in_json)

    if not(clients.chek_priv(g.token, 'doc_action_post')):
        app.logger.debug('<Resp: {} >'.format('[NO PRIVILEGE] - doc_action_post'))
        return make_response(jsonify({'ERROR': 'NO PRIVILEGE - doc_action_post'}), 403)

    try:
        if 'IDSMR' in in_json:
            IDSMR                       = in_json['IDSMR']                  # ID Банка (Филиала), где зарегистрирован документ
        else:
            IDSMR = None
# Данные  документа
        if 'DATE_DOC' in in_json:
            DATE_DOC                    = in_json['DATE_DOC']               # Дата документа
        else:
            DATE_DOC = None
        if 'NUM_DOC' in in_json:
            NUM_DOC                     = in_json['NUM_DOC']                # Номер документа
        else:
            NUM_DOC = None
# Клиент
        if 'CLN_BNK_NAME' in in_json:
            CLN_BNK_NAME                = in_json['CLN_BNK_NAME']
        else:
            CLN_BNK_NAME = None
        if 'CLN_NAME' in in_json:
            CLN_NAME                    = in_json['CLN_NAME']
        else:
            CLN_NAME    = None
        if 'CLN_INN' in in_json:
            CLN_INN                     = in_json['CLN_INN']
        else:
            CLN_INN = None
        if 'CLN_OKPO' in in_json:
            CLN_OKPO                    = in_json['CLN_OKPO']
        else:
            CLN_OKPO    = None
        if 'CLN_ADDR' in in_json:
            CLN_ADDR                    = in_json['CLN_ADDR']
        else:
            CLN_ADDR    = None
        if 'CLN_EMPLOYEE_FIO' in in_json:
            CLN_EMPLOYEE_FIO            = in_json['CLN_EMPLOYEE_FIO']
        else:
            CLN_EMPLOYEE_FIO    = None
        if 'CLN_EMPLOYEE_PHONES' in in_json:
            CLN_EMPLOYEE_PHONES         = in_json['CLN_EMPLOYEE_PHONES']
        else:
            CLN_EMPLOYEE_PHONES = None
# Списание рублей
        if 'SALE_SUM' in in_json:
            SALE_SUM = in_json['SALE_SUM']
        else:
            SALE_SUM = None
        if 'SALE_CURRENCY' in in_json:
            SALE_CURRENCY               = in_json['SALE_CURRENCY']
        else:
            SALE_CURRENCY   = None
        if 'SALE_ACCOUNT' in in_json:
            SALE_ACCOUNT = in_json['SALE_ACCOUNT']
        else:
            SALE_ACCOUNT = None
# Курс конвертации
        if 'CONVERT_RATE_KIND' in in_json:
            CONVERT_RATE_KIND = in_json['CONVERT_RATE_KIND']
        else:
            CONVERT_RATE_KIND = None
        if 'CONVERT_RATE' in in_json:
            CONVERT_RATE = in_json['CONVERT_RATE']
        else:
            CONVERT_RATE = None
# Зачисление валюты
        if 'BUY_SUM' in in_json:
            BUY_SUM = in_json['BUY_SUM']
        else:
            BUY_SUM = None
        if 'BUY_CURRENCY' in in_json:
            BUY_CURRENCY = in_json['BUY_CURRENCY']
        else:
            BUY_CURRENCY = None
        if 'BUY_ACCOUNT' in in_json:
            BUY_ACCOUNT = in_json['BUY_ACCOUNT']
        else:
            BUY_ACCOUNT = None
# Дополнительно
        if 'EXPERIENCE_DATE' in in_json:
            EXPERIENCE_DATE = in_json['EXPERIENCE_DATE']
        else:
            EXPERIENCE_DATE = None
        if 'TRANSFER_DATE' in in_json:
            TRANSFER_DATE = in_json['TRANSFER_DATE']
        else:
            TRANSFER_DATE = None
        if 'ADDED_COND' in in_json:
            ADDED_COND = in_json['ADDED_COND']
        else:
            ADDED_COND = None
# Подписи
        if 'VCSIGN1' in in_json:
            VCSIGN1 = in_json['VCSIGN1']  # Подпись первого лица
        else:
            VCSIGN1 = None
        if 'VCSIGN2' in in_json:
            VCSIGN2 = in_json['VCSIGN2']  # Подпись второго лица
        else:
            VCSIGN2 = None
# Идентификация
        if 'CID' in in_json:
            CID = in_json['CID']  # Внешний iD документа (Идентификатор платежа в системе Банк-Клиент)
        else:
            CID = None
        if 'CIP' in in_json:
            CIP = in_json['CIP']  # IP-адрес, с которого был отправле документ
        else:
            CIP = None
        if 'CMAC' in in_json:
            CMAC = in_json['CMAC']  # MAC-адрес, с которого был отправле документ
        else:
            CMAC = None
    except:
     app.logger.error('Possible incorrect format of json body in POST !')
     return bad_request(400)

    try:
        if ((IDSMR == '1') or (IDSMR == '')):
            con = absdb.set_connection(absdb.db_user, absdb.db_user_pwd)
            cur = con.cursor()
        elif IDSMR == '2':
            f1con = absdb.set_connection(absdb.db_f1user, absdb.db_f1user_pwd)
            cur = f1con.cursor()
        elif IDSMR == '3':
            f2con = absdb.set_connection(absdb.db_f2user, absdb.db_f2user_pwd)
            cur = f2con.cursor()
        else:
            return bad_request(400)
    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error('[ERROR] DB Connection ERROR!')
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return not_available(503)

    RESCODE = cur.var(int)  # Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    RETMSG = cur.var(absdb.db.STRING)  # Строка с сообщением о результате
    DOCID = cur.var(absdb.db.STRING)  # Идентификатор документа в формате "doctype_inum_ianum"

    try:
        cur.callproc('isb_abs_api_docs.REG_VAL_CONVERT', [
            IDSMR,
        # Данные  документа
            DATE_DOC,
            NUM_DOC,
        # Клиент
            CLN_BNK_NAME,
            CLN_NAME,
            CLN_INN,
            CLN_OKPO,
            CLN_ADDR,
            CLN_EMPLOYEE_FIO,
            CLN_EMPLOYEE_PHONES,
        # Списание
            SALE_SUM,
            SALE_CURRENCY,
            SALE_ACCOUNT,
        # Курс конвертации
            CONVERT_RATE_KIND,
            CONVERT_RATE,
        # Зачисление
            BUY_SUM,
            BUY_CURRENCY,
            BUY_ACCOUNT,
        # Дополнительно
            EXPERIENCE_DATE,
            TRANSFER_DATE,
            ADDED_COND,
        # Подписи
            VCSIGN1,
            VCSIGN2,
        # Идентификация
            CID,
            CIP,
            CMAC,
        # Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}

    except absdb.db.Error as exc:
        error, = exc.args
        app.logger.error("Oracle-Error-Code: {}".format(error.code))
        app.logger.error("Oracle-Error-Message: {}".format(error.message))
        return internal_error(500)

    if RESCODE.getvalue() > 0:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 201)
    else:
        app.logger.debug('<Resp: {} >'.format(j_rez))
        return make_response(jsonify(j_rez), 200)

########################################################################################################################
def geta_doc_service_settings(ini_path):

    if not os.path.exists(ini_path):
        app.logger.error("[ERROR] No ini files found")
        exit()
    else:
        config = configparser.ConfigParser()
        config.read(ini_path)

    # Читаем значения из конфиг. файла.
        l_doc_ip = config.get("SERVECES SETTINGS", "doc_ip")
        l_doc_port = config.get("SERVECES SETTINGS", "doc_port")
        l_ssl_cerf_file = config.get("SERVECES SETTINGS", "ssl_cert_file")
        l_ssl_key_file = config.get("SERVECES SETTINGS", "ssl_key_file")

    return (l_doc_ip, l_doc_port, l_ssl_cerf_file, l_ssl_key_file)

########################################################################################################################

doc_service_ip, doc_service_port, ssl_cert, ssl_key = geta_doc_service_settings("absgate.ini")

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
            debug=True, host=doc_service_ip, port=doc_service_port)