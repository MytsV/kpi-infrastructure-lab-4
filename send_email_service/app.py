import pika
import json
from decouple import config

def callback(ch, method, properties, body):
    message = json.loads(body)
    # Append logs file
    with open('logs.txt', 'a') as file:
        file.write(f"Sent email to {message['email']}: {message['message']}\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('rabbitmq')
    )
    channel = connection.channel()
    channel.queue_declare(queue=config('RABBITMQ_EMAIL_QUEUE'), durable=True)
    channel.basic_consume(queue=config('RABBITMQ_EMAIL_QUEUE'), on_message_callback=callback)
    print("Waiting for SMS messages. To exit, press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    main()
