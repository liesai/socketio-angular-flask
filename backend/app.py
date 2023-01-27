from flask_socketio import SocketIO, send, emit
from flask import Flask, jsonify, request
from flask_cors import CORS
import pika

app = Flask(__name__)
CORS(app)

socketio = SocketIO(app, logger=True, engineio_logger=True,
                    cors_allowed_origins="*")

wishlist = []


@app.route('/wishlist', methods=['GET', 'POST'])
def manage_wishlist():
    if request.method == 'POST':
        item = request.get_json()
        wishlist.append(item)
        return jsonify({'success': True}), 201
    elif request.method == 'GET':
        return jsonify(wishlist)


@app.route("/amq", methods=['POST'])
def amq():
    result = []
    test = request.get_json()
    result.append(test)

    socketio.emit('topico', result, broadcast=True)
    return jsonify(result)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
