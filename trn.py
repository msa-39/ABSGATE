# Микросервис API для работы с проводками

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/absapi/v1/trn', methods=['POST'])
# Register PayMent
def RegPayment():
    return make_response("[Ok] RegPayment\n", 200)


if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5003)