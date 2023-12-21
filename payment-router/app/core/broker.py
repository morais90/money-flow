import json

import pika


def push_to_queue(queue_name: str, payload: dict):
    connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange="", routing_key="hello", body=json.dumps(payload))

    connection.close()
