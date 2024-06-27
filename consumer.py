import pika
import logging
from bson import BSON

logging.basicConfig(filename='example.log', level=logging.INFO)

def on_message(channel, method_frame, header_frame, body):
    logging.info(method_frame.delivery_tag)
    logging.info(BSON(body).decode())
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.basic_consume('hello', on_message)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()