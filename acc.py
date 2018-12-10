# Микросервис API для работы со счетами

from flask import Flask, request, make_response
import json
from dbutills import absdb

app = Flask(__name__)

@app.route('/absapi/v1/acc/<int:iacccur>/<int:iaccacc>', methods=['GET'])
# Get information about Account
def GetAccInfo(iacccur, iaccacc):
    return make_response("[Ok] GetAccInfo\n Acc = "+str(iaccacc), 200)

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


if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5001)