from threading import Thread
from flask_socketio import SocketIO, send, emit
from flask import Flask, jsonify, request
from flask_cors import CORS
import pika
import json
import time

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


def callback(ch, method, properties, body):
    # votre logique de traitement du message ici
    print("{X] AMQ ---- Received message: ", body)
    data = []
    time.sleep(2)
    jsonToSend = json.loads(body.decode('utf-8'))
    data.append(jsonToSend)
    print(data)

    socketio.emit('topico', data, broadcast=True)


def start_consuming():
    credentials = pika.PlainCredentials('python', 'G!tK_P_ZmB4qUUV')

    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost', heartbeat=60, credentials=credentials))

    except pika.AMQPConnectionError as e:
        print(f'connexion failed : {e}')

    channel = connection.channel()
    channel.queue_declare(queue='toctoc')
    channel.basic_consume(queue='toctoc', on_message_callback=callback)
    print('Start consuming')
    channel.start_consuming()


def main():
    consumer_thread = Thread(target=start_consuming)
    consumer_thread.start()


main()

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
