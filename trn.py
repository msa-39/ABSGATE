# Микросервис API для работы с проводками

from flask import Flask, jsonify, make_response, request
import json
from dbutills import absdb
from flask_httpauth import HTTPTokenAuth

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


@app.route('/absapi/v1/trn', methods=['POST'])
# Register PayMent
def RegPayment():
    return make_response("[Ok] RegPayment\n", 200)




if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5003)