# Микросервис API для работы с клиентами

from flask import Flask, jsonify, make_response, request
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth
from utills import clients
import json
import logging

#logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.DEBUG, filename=u'abs_api_cus.log')

app = Flask(__name__)

auth = HTTPTokenAuth('Bearer')

@auth.verify_token
def verify_token(token):
    return clients.check_key(token)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/absapi/v1/cus', methods=['GET'])
#@auth.login_required
# Get short information about ALL Custimers, hwo has opened account
def GetCusAll():
    inn = request.args.get('inn')
    inn = (inn or '')
    con = None
    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = "select isb_abs_api_cus.get_all_cus_info(:inn) from dual"
    cu.execute(plSQL, inn=inn)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)

@app.route('/absapi/v1/cus/<int:icusnum>', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusInfo(icusnum):
    res = None
    con = None
    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = "select isb_abs_api_cus.get_cus_info(:icusnum) from dual"
    cu.execute(plSQL, icusnum=icusnum)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/fullinfo', methods=['GET'])
#@auth.login_required
# Get FULL information about Custimer by icusnum
def GetCusFullInfo(icusnum):
    res = None
    con = None
    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = "select isb_abs_api_cus.get_cus_full_info(:icusnum) from dual"
    cu.execute(plSQL, icusnum=icusnum)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)

#    return make_response(jsonify({'msg': '[Ok] GetCusFullInfo CusNum = '+str(icusnum)}), 200)




@app.route('/absapi/v1/cus/<int:icusnum>/docums', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusDocumsInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusDocumsInfo CusNum = '+str(icusnum)}), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/addresses', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusAddressesInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusAddressesInfo CusNum = '+str(icusnum)}), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/phonefaxes', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusPhoneFaxesInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusPhoneFaxesInfo CusNum = '+str(icusnum)}), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/ruks', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusRuksInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusRuksInfo CusNum = '+str(icusnum)}), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusBankProductsInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusBankProductsInfo CusNum = '+str(icusnum)}), 200)

@app.route('/absapi/v1/cus/<int:icusnum>/bankproducts/credits', methods=['GET'])
#@auth.login_required
# Get short information about Custimer by icusnum
def GetCusCreditsInfo(icusnum):
    return make_response(jsonify({'msg': '[Ok] GetCusCreditsInfo CusNum = '+str(icusnum)}), 200)

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

if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5002)