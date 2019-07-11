"""Example 06: worker part.

Synopsis: this script will listen to messages (tasks) published to ex_06_tasks queue
and then publish back results.
"""
from examples.config import CONN_PARAMETERS
import pika

QUEUE_NAME = 'ex_06_tasks'  # Queue to which "tasks" will arrive


def fibonacci(n):
    """Naive recursive implementation of computing Fibonacci sequence."""
    if n <= 1:
        return n

    return fibonacci(n-1) + fibonacci(n-2)


def on_message(channel, method, properties, body):
    """Message callback."""
    n = int(body)              # Get the argument
    response = fibonacci(n)    # Compute response

    channel.basic_publish(
        exchange='',
        routing_key=properties.reply_to,
        properties=pika.BasicProperties(correlation_id=properties.correlation_id),
        body=str(response)
    )

    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
        print('Starting consuming...')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Finished consuming.')


if __name__ == '__main__':
    main()
