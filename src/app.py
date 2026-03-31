#'/api/v1/details'
from flask import Flask, jsonify
from datetime import datetime
import socket

app = Flask(__name__)

@app.route('/api/v1/details')
def details():
    now = datetime.now()
    hostName = socket.gethostname()
    return jsonify({'time': now.strftime("%H:%M:%S"),
                    'hostName': hostName })

@app.route('/api/v1/healthz')
def health():
    return jsonify({'status': 'up', }), 200

if __name__ == '__main__':
    app.run(host= "0.0.0.0")
#'/api/v1/healthz'