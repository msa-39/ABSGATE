# Микросервис API для работы с клиентами

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/absapi/v1/cus', methods=['GET'])



if __name__ == '__main__':
    app.run(ssl_context=('/home/moiseev/cert.pem', '/home/moiseev/key.pem'),
            debug=True, host='0.0.0.0', port=5003)