# utils/rabbitmq.py
from django.conf import settings
import pika
import json

def send_message(queue, message):
    try:
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(settings.RABBITMQ['HOST'])
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue, durable=True)
        channel.basic_publish(exchange='', routing_key=queue, body=json.dumps(message))
        print(f"Message sent to {queue}", flush=True)
        connection.close()
    except Exception as e:
        print(f"Error sending message to {queue}: {e}", flush=True)
        raise
