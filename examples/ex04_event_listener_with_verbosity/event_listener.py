"""Example 03: Event listener.

Synopsis: running this script will bind temporary queue to ex_04_events exchange with possibly multiple routing
keys corresponding to event types. This example will get event types from command line, so it is possible to run
it with different "verbosity".
"""
import json
import sys
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_04_events'  # Exchange to which events will be published


def on_message(channel, method, properties, body):
    event = json.loads(body.decode('utf-8'))
    print(event['ts'], event['event_type'])


def main():
    """Entry point of this script."""

    event_types = sys.argv[1:] # 0-th argument is the scripts path, so we take event types from other args

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

        result = channel.queue_declare(queue='', exclusive=True)

        # Bind temporary queue to our exchange. We use separate binding for each event type

        for event_type in event_types:
            channel.queue_bind(exchange=EXCHANGE, queue=result.method.queue, routing_key=event_type)

        channel.basic_consume(queue=result.method.queue, on_message_callback=on_message, auto_ack=True)

        print(f'Waiting for messages on queue {result.method.queue}')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Finished consuming.')


if __name__ == '__main__':
    main()
