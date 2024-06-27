import pymongo
import logging
import pika
from bson import BSON

logging.basicConfig(filename='example.log', level=logging.DEBUG)

db = pymongo.MongoClient('mongodb://mongo1:27017/')
db = db.test
logging.info('conectando...')
try:
    resume_token = None
    #pipeline = [{'$match': {'operationType': 'insert'}}]
    with db.jorge.watch() as stream:
        for insert_change in stream:
            logging.info('----------------')
            logging.info(insert_change)
            logging.info('----------------')
            resume_token = stream.resume_token 

            connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
            channel = connection.channel()

            channel.queue_declare(queue='hello')

            channel.basic_publish(exchange='',
                                routing_key='hello',
                                body=BSON.encode(insert_change))
            print(" [x] Sent 'Hello World!'")
            connection.close()

except pymongo.errors.PyMongoError as e:
    # The ChangeStream encountered an unrecoverable error or the
    # resume attempt failed to recreate the cursor.
    if resume_token is None:
        # There is no usable resume token because there was a
        # failure during ChangeStream initialization.
        logging.info(e)
    else:
        # Use the interrupted ChangeStream's resume token to create
        # a new ChangeStream. The new stream will continue from the
        # last seen insert change without missing any events.
        logging.info('??????')
        with db.collection.watch(
                pipeline, resume_after=resume_token) as stream:
            for insert_change in stream:
                print(insert_change)