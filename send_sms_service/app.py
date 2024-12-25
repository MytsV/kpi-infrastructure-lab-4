import logging
import pika
import json
from decouple import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def callback(ch, method, properties, body):
    message = json.loads(body)
    phone_number = message['phone_number']
    if phone_number is None:
        logger.warning("Can't send SMS to an entity without a phone_number")
    else:
        logger.info(f"Sent an SMS to {phone_number} with text: {message['message']}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    rabbitmq_host = config('RABBITMQ_HOST')
    rabbitmq_port = config('RABBITMQ_PORT')
    rabbitmq_user = config('RABBITMQ_USER')
    rabbitmq_password = config('RABBITMQ_PASSWORD')

    credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            credentials=credentials
        )
    )
    channel = connection.channel()
    logger.info("Established connection with RabbitMQ.")
    channel.queue_declare(queue=config('RABBITMQ_SMS_QUEUE'), durable=True)
    channel.basic_consume(queue=config('RABBITMQ_SMS_QUEUE'), on_message_callback=callback)
    channel.start_consuming()


if __name__ == "__main__":
    main()
