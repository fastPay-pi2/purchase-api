from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
import json as js
import logging

FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
logging.basicConfig(
    # filename='logfile.txt',
    # filemode='a',
    level=logging.DEBUG,
    format=FORMAT
)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app)
socketio = SocketIO(app)

@socketio.on('my event')
def handle_message(json, methods=['GET', 'POST']):
    print('@@@received message: ' + js.dumps(json, indent=2))
    socketio.emit('response', {'msg': 'ooooooook'})

@socketio.on('connected')
def connected():
    print('#######')
    print(request)

@app.route('/')
def hello():
    name = 'Hello World'
    return {'msg': name}

if __name__ == '__main__':
    socketio.run(app, port=5001)
    logging.debug('Server is running')