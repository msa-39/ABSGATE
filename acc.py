# Микросервис API для работы со счетами

import datetime
from flask import Flask, jsonify, make_response, request
import json
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth
from utills import clients

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


@app.route('/absapi/v1/acc/<int:p_idsmr>/<string:p_cacccur>/<int:p_iaccacc>/info', methods=['GET'])
# Get information about Account

def GetAccInfo(p_idsmr, p_cacccur, p_iaccacc):

    caccacc = str(p_iaccacc)
    cacccur = p_cacccur
    cidsmr = str(p_idsmr)
    res = None
    con = None

    try:
        if ((len(caccacc) != 20) or (len(cacccur) != 3)):
            raise Exception("Bad request")
    except:
        return bad_request(400)

    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_acc.get_acc_info(:p_caccacc, :p_cacccur, :p_idsmr)) from dual"
    cu.execute(plSQL, p_caccacc=str(p_iaccacc), p_cacccur=p_cacccur, p_idsmr=p_idsmr)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)


@app.route('/absapi/v1/acc/<int:p_idsmr>/<string:p_cacccur>/<int:p_iaccacc>/statement/<int:p_date_from>/<int:p_date_to>', methods=['GET'])
# Get Statement of Account from date_from to date_to

def GetAccStatement(p_idsmr, p_cacccur, p_iaccacc, p_date_from, p_date_to):
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
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')

    cu = con.cursor()

    res = cu.callfunc('isb_abs_api_acc.get_acc_statement_clob',
                      absdb.db.CLOB,
                      [caccacc, cacccur, cidsmr, begin_date, end_date])

    return make_response(jsonify(json.loads(res.read())), 200)

    #plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_acc.get_acc_statement(:p_caccacc, :p_cacccur, :p_idsmr, :p_date_from, :P_date_to)) from dual"
    #cu.execute(plSQL, p_caccacc=str(p_iaccacc), p_cacccur=p_cacccur, p_idsmr=p_idsmr, p_date_from=p_date_from, p_date_to=p_date_to)
    #res=cu.fetchall()
    #return make_response(jsonify(json.loads(res[0][0].read())), 200)

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

if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5001)