"""Example 03: Event listener.

Synopsis: running this script will bind temporary queue, bind it to ex_03_events exchange and consume for the queue.
The temporary queue will be deleted upon listener's exit.
"""
import json
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_03_events'  # Exchange to which events will be published


def on_message(channel, method, properties, body):
    event = json.loads(body.decode('utf-8'))
    print(event['ts'], event['event_type'])


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # We declare exchange - publishing to nonexisting exchange would result in an exception.
        # This operation, just like declaring a queue, is idempotent.
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        # Create randomly named exclusive (think: temporary) queue. We don't need to generate name ourselves,
        # specifying an empty name will cause broker to generate name.
        result = channel.queue_declare(queue='', exclusive=True)

        # Bind temporary queue to our exchange.
        channel.queue_bind(exchange=EXCHANGE, queue=result.method.queue)

        channel.basic_consume(queue=result.method.queue, on_message_callback=on_message, auto_ack=True)

        print(f'Waiting for messages on queue {result.method.queue}')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Finished consuming.')


if __name__ == '__main__':
    main()
