# -*- coding: utf-8 -*-

from flask import Flask, request, jsonify
import time
import random
from datetime import datetime
import psycopg2

app = Flask(__name__, static_url_path='/assets')

TOKEN_ALPH = 'UCTF137'
TEAPOT = '500.webp'


@app.route('/')
def serve_index():
    return app.send_static_file('index.html')


@app.route('/api/apply', methods=['POST'])
def apply():
    conn = psycopg2.connect("host=10.239.0.250 dbname=db user=writer password=DrARYwy523")
    conn.set_client_encoding('UTF8')
    token = request.form.get('token')
    try:
        data = {
            'plan': int(token.split('.')[1]),
            'timestamp': int(time.time()),
            'token': ''.join([random.choice(TOKEN_ALPH) for _ in range(10)])
        }
        if data['plan'] == 1:
            data['active_on'] = data['timestamp'] + 60
            data['name'] = 'Kaefный'
        else:
            data['active_on'] = data['timestamp'] + 2592000

        cur = conn.cursor()
        cur.execute("INSERT INTO request (token, date, activated) VALUES (%s, %s, false)", (data["token"], datetime.fromtimestamp(data["active_on"])))
        conn.commit()
        cur.close()
        return jsonify(data)

    except IndexError:
        return app.send_static_file(TEAPOT)


@app.errorhandler(404)
def serve_404(error):
    return app.send_static_file(TEAPOT)


if __name__ == "__main__":
    app.run(debug=True)
