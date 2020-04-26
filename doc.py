# Микросервис API для работы с проводками

from flask import Flask, jsonify, make_response, request
import json
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth
from utills import clients
import re
import logging

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, filename=u'abs_api_doc.log')

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

auth = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    return clients.check_key(token)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'ERROR': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'ERROR': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'ERROR': 'Not found'}), 404)

@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify({'ERROR': 'Internal error'}), 500)

@app.errorhandler(503)
def not_available(error):
    return make_response(jsonify({'ERROR': 'Service Unavailable'}), 503)

########################################################################################################################
@app.route('/absapi/v1/doc/<string:p_docid>', methods=['GET'])
# Get document (transaction) information

# Требуется авторизация
#@auth.login_required
def GetTrnInfo(p_docid):

    try:
        l_doctype = re.match(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))', p_docid).group(0).upper()
        p_docid   =   re.sub(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))', '', p_docid)
        l_inum = int(re.match(r'\d+', p_docid).group(0))
        l_ianum = int(re.sub(r'\d+_', '', p_docid))

    except:
        return bad_request(400)

    try:
        con = absdb.set_connection()
        cur = con.cursor()
    except:
        print('[ERROR] DB Connection ERROR!')
        return not_available(503)

    plSQL = ''

    if re.fullmatch(r'TRN', l_doctype):
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_docs.get_trn_info(:p_itrnnum, :p_itrnanum)) from dual"

    if (len(plSQL) == 0):
        return bad_request(400)

    try:
        cur.execute(plSQL, p_itrnnum=l_inum, p_itrnanum=l_ianum)
        res=cur.fetchall()
        return make_response(jsonify(json.loads(res[0][0].read())), 200)
    except:
        return internal_error(500)

########################################################################################################################
@app.route('/absapi/v1/doc', methods=['POST'])
# Register RUR PayMent

# Требуется авторизация
@auth.login_required

def RegRURPayment():

    in_json = request.json

    #print(json.dumps(in_json))
    #print(in_json)

    try:
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

        CTRNPURP        =   in_json['CTRNPURP']               # Назначение платежа
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

        CSIGN1_FIO      =   in_json['CSIGN1_FIO']             # ФИО (Подпись) первого лица
        CSIGN2_FIO      =   in_json['CSIGN2_FIO']             # ФИО (Подпись) второго лица

        CID             =   in_json['CID']                    # Идентификатор платежа в системе Банк-Клиент
        CIP             =   in_json['CIP']                    # IP-адрес, с которого был отправле документ
        CMAC            =   in_json['CMAC']                   # MAC-адрес, с которого был отправле документ

    except:
        return bad_request(400)

    try:
        con = absdb.set_connection()
        cur = con.cursor()
    except:
        print('[ERROR] DB Connection ERROR!')
        return not_available(503)

    RESCODE     =   cur.var(int)                  #  Код результата выполнения процедуры (-1 - ERROR; 1 - Документ зарегистрирован; 2 - Документ в Отложенные; 3 - Документ на Картотеку)
    #ResCode.setvalue(0,-1)

    RETMSG      =   cur.var(absdb.db.STRING)      #  Строка с сообщением о результате
    #RetMsg.setvalue(0, '')

    DOCID       =   cur.var(absdb.db.STRING)      #  Идентификатор документа в формате "doctype_inum_ianum"
    #DOCID.setvalue(0, '')

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
            CTRNPURP,
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
# Выходные параметры
            RESCODE,
            RETMSG,
            DOCID
        ])

        j_rez = {'RESCODE': RESCODE.getvalue(),
                 'RETMSG': RETMSG.getvalue(),
                 'DOCID': DOCID.getvalue()}
    except:
        return internal_error(500)

    if RESCODE.getvalue()>0:
        return make_response(jsonify(j_rez), 201)
    else:
        return make_response(jsonify(j_rez), 200)

########################################################################################################################

if __name__ == '__main__':
    app.run(ssl_context=('cert2019.pem', 'key2019.pem'),
            debug=True, host='0.0.0.0', port=5003)