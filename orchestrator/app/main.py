import orjson
import pika

from app.core.settings import settings
from app.workflows import Context, create_workflow


def callback(ch, method, properties, body):
    event = orjson.loads(body)
    payment = event["payment"]
    context = Context(
        {
            "payment": event["payment"],
            "company": event["company"],
        }
    )

    # TODO: Support Dask Distributed
    # TODO: Error handling and retry policy
    workflow = create_workflow(payment["type"])
    workflow(context=context, rules=event["rules"])

    ch.basic_ack(delivery_tag=method.delivery_tag)


# TODO: Tolerance for failures
def main():
    connection = pika.BlockingConnection(pika.URLParameters(str(settings.RABBITMQ_DSN)))
    channel = connection.channel()

    channel.queue_declare(queue="payment", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="payment", on_message_callback=callback, auto_ack=False)

    channel.start_consuming()


if __name__ == "__main__":
    main()
