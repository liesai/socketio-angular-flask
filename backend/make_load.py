import requests
import random
import string
import json
from threading import Thread
import pika


x = 0
letters = string.ascii_lowercase
credentials = pika.PlainCredentials('pika_user', 'pika_password')

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', heartbeat=60, credentials=credentials))
    print('connected')

except pika.AMQPConnectionError as e:
    print(f'connexion failed : {e}')


def send_data_to_topic(topic, payload):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    if connection.is_open:
        channel = connection.channel()
        channel.exchange_declare(exchange=topic, exchange_type='topic')
        channel.queue_bind(queue='toctoc', exchange=topic,
                           routing_key='toctoc')
        channel.basic_publish(exchange=topic, routing_key=topic, body=payload)
        print(" [x] Sent %r:%r" % (topic, payload))
        connection.close()
    else:
        print("Connection is closed, unable to send message.")


while True:
    topic = "toctoc"
    url = "http://localhost:5000/amq"
    payload = json.dumps({'offerId': x, 'status':
                          ''.join(random.choice(letters) for i in range(10))})
    headers = {
        'Content-Type': 'application/json'
    }
    x += 1
    # r = requests.request('POST', url, headers=headers, data=payload)
    # print(f'send data [x] #{x} {payload} - status: {r.status_code} ')
    send_data_to_topic(topic, payload)
