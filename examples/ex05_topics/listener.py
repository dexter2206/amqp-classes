"""Example 05: measurement listener

Synopsis: this listener will consume messages published to ex_05_measurement, filtered by topic
read from command line parameter. We will use it to listen for messages posted for given room
or message concerning given quantity.
"""
import sys
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_05_measurements'  # Exchange to which events will be published


def on_message(channel, method, properties, body):
    print(method.routing_key, body.decode('utf-8'))


def main():
    """Entry point of this script."""

    routing_key = sys.argv[1]  # Get routing key from command line

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

        result = channel.queue_declare(queue='', exclusive=True)

        channel.queue_bind(exchange=EXCHANGE, queue=result.method.queue, routing_key=routing_key)

        channel.basic_consume(queue=result.method.queue, on_message_callback=on_message, auto_ack=True)

        print(f'Waiting for messages on queue {result.method.queue}')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Finished consuming.')


if __name__ == '__main__':
    main()
