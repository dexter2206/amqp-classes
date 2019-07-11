"""Example 01: basic example of AMQP consumer"""
from examples.config import CONN_PARAMETERS
import pika

QUEUE_NAME = 'hello_world'


def on_message(channel, method, properties, body):
    """Callback invoked when message is received."""
    print(f'Obtained message: {body.decode("utf-8")}')


def main():
    """Entry point of this script."""
    # Create connection to the broker
    conn = pika.BlockingConnection(CONN_PARAMETERS)

    # Create channel for communication with broker.
    # Remember that channel (not a connection!) is a basic unit of communication with broker.
    channel = conn.channel()

    # Make sure queue exists. Declaring queue is idempotent (i.e. declaring queue multiple times has no effect)*.
    channel.queue_declare(queue=QUEUE_NAME)

    # Declare that we want to consume messages from 'hello_world
    channel.basic_consume(queue=QUEUE_NAME, auto_ack=True, on_message_callback=on_message)

    # As a last step for consumption, we need to start consumer loop.
    print('Starting consumption, hit Ctrl-C to finish...')

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print('Finished consuming.')

    conn.close()


if __name__ == '__main__':
    main()
