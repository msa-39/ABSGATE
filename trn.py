# Микросервис API для работы с проводками

from flask import Flask, jsonify, make_response, request
import json
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth
import re

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

auth = HTTPTokenAuth('Bearer')

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


@app.route('/absapi/v1/trn/document/<string:itrnnum_itrnanum>', methods=['GET'])
# Get document (transaction) information

#@auth.login_required
def GetTrnInfo(itrnnum_itrnanum):

    l_itrnnum = int(re.match(r'\d+', itrnnum_itrnanum).group(0))
    l_itrnanum = int(re.sub(r'\d+_', '', itrnnum_itrnanum))

    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_trn.get_trn_info(:p_itrnnum, :p_itrnanum)) from dual"
    cu.execute(plSQL, p_itrnnum=l_itrnnum, p_itrnanum=l_itrnanum)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)


@app.route('/absapi/v1/trn', methods=['POST'])
# Register PayMent
def RegPayment():
    return make_response("[Ok] RegPayment\n", 200)




if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5000)