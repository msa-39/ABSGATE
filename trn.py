# Микросервис API для работы с проводками

from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

@app.route('/absapi/v1/trn', methods=['POST'])