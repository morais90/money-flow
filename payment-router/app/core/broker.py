import json

import pika

from app.core.settings import settings


def push_to_queue(queue_name: str, payload: dict):
    """Push a payload to a queue

    Args:
        queue_name (str): Queue name
        payload (dict): An arbitrary dictionary
    """

    connection = pika.BlockingConnection(pika.URLParameters(str(settings.RABBITMQ_DSN)))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="payment",
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )

    connection.close()
