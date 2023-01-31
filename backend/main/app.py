from threading import Thread
from flask_socketio import SocketIO, send, emit
from flask import Flask, jsonify, request, Blueprint
import pika
import json
from flask_cors import CORS
import mysql.connector


mysql_host = "127.0.0.1"
mysql_user = "root"
mysql_password = "password"
mysql_database = "service_offre"


app = Flask(__name__)

socketio = SocketIO(app, logger=True, engineio_logger=True,
                    cors_allowed_origins="*", ping_timeout=10)
cors = CORS(app)


global credentials
credentials = pika.PlainCredentials('python', 'G!tK_P_ZmB4qUUV')
global connexion
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', heartbeat=60, credentials=credentials))


def access_db(payload):
    result = []
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host, database=mysql_database)
    cursor = cnx.cursor()
    query = ("SELECT id_offre, status FROM offres WHERE id_offre LIKE %s")
    cursor.execute(query, (payload['offerId'],))
    if cursor.fetchone():
        print(f"{payload['offerId']} already exists")
        result.append(payload)

    else:
        add_offer = ("INSERT INTO offres (id_offre, status) VALUES (%s, %s)")
        data_offer = (payload['offerId'], payload['status'])
        cursor.execute(add_offer, data_offer)
        cnx.commit()
        socketio.emit('topico', result, broadcast=True)
    cursor.close()
    cnx.close()


@app.route("/amq", methods=['GET'])
def get_data():
    result = []
    cnx = mysql.connector.connect(user=mysql_user, password=mysql_password,
                                  host=mysql_host, database=mysql_database)
    cursor = cnx.cursor()
    query = ("SELECT id_offre, status FROM offres LIMIT 10")
    cursor.execute(query)
    for id_offre, status in cursor:
        _result = {'offerId': id_offre, 'status': status}
        result.append(_result)
    return jsonify(result)


@app.route("/api/amq", methods=['POST', 'GET'])
def amq():
    result = []
    test = request.get_json()
    print(test)
    result.append(test)
    access_db(test)
    return jsonify(result)


def callback(ch, method, properties, body):

    print("{X] AMQ ---- Received message: ", body)
    data = []
    jsonToSend = json.loads(body.decode('utf-8'))
    data.append(jsonToSend)
    access_db(jsonToSend)
    # with app.app_context():
    #     access_db(jsonToSend)

    socketio.emit('topico', data, broadcast=True)


def start_consuming():

    channel = connection.channel()
    channel.queue_declare(queue='toctoc')
    channel.basic_consume(queue='toctoc', on_message_callback=callback)
    print('Start consuming')
    channel.start_consuming()


def start_thread():

    consumer_thread = Thread(target=start_consuming)
    consumer_thread.start()


start_thread()
if __name__ == '__main__':

    socketio.run(app, host='0.0.0.0', port=8080)
