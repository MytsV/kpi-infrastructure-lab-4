from django.conf import settings
import pika
import json


def send_message(queue, message):
    try:
        rabbitmq_host = settings.RABBITMQ['HOST']
        rabbitmq_port = settings.RABBITMQ['PORT']
        rabbitmq_user = settings.RABBITMQ['USER']
        rabbitmq_password = settings.RABBITMQ['PASSWORD']

        credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=credentials
            )
        )

        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message), properties=pika.BasicProperties(
            delivery_mode=2
        ))
        print(f"Message sent to {queue}", flush=True)
        connection.close()
    except Exception as e:
        print(f"Error sending message to {queue}: {e}", flush=True)
        raise
