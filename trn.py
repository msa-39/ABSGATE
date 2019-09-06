# Микросервис API для работы с проводками

from flask import Flask, jsonify, make_response, request
import json
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth
from utills import clients
import re

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


@app.route('/absapi/v1/document/<string:p_docid>', methods=['GET'])
# Get document (transaction) information

#@auth.login_required
def GetTrnInfo(p_docid):

    try:
        l_doctype = re.match(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))', p_docid).group(0).upper()
        p_docid   =   re.sub(r'((t|T)(r|R)(n|N)|(t|T)(r|R)(c|C)|(d|D)(p|P)(d|D))_', '', p_docid)
        l_inum = int(re.match(r'\d+', p_docid).group(0))
        l_ianum = int(re.sub(r'\d+_', '', p_docid))

    except:
        return bad_request(400)

    try:
        con = absdb.set_connection()
    except:
        print('[ERROR] DB Connection ERROR!')
    cu = con.cursor()
    plSQL = ''

    if re.fullmatch(r'TRN', l_doctype):
        plSQL = "select isb_abs_api_util.pljson_value2clob(isb_abs_api_trn.get_trn_info(:p_itrnnum, :p_itrnanum)) from dual"

    if (len(plSQL) == 0):
        return bad_request(400)

    cu.execute(plSQL, p_itrnnum=l_inum, p_itrnanum=l_ianum)
    res=cu.fetchall()
    return make_response(jsonify(json.loads(res[0][0].read())), 200)

#    print(plSQL)
#    return "l_doctype = "+l_doctype+"</br> l_inum = "+str(l_inum)+"</br> l_ianum = "+str(l_ianum)


@app.route('/absapi/v1/trn', methods=['POST'])
# Register PayMent
def RegPayment():
    return make_response("[Ok] RegPayment\n", 200)




if __name__ == '__main__':
    app.run(ssl_context=('cert.pem', 'key.pem'),
            debug=True, host='0.0.0.0', port=5003)