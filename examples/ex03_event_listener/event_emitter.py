"""Example 03: Event emitter.

Synopsis: running this script will publish json-encoded message (an event) to ex_03_events exchange.
This events are meant to be consumed by event_listener.py

This example is a first one that will not use the default exchange, and also an example of publishing to
fanout exchange.
"""
from time import time
import json
import random
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_03_events'  # Exchange to which events will be published


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # We declare exchange - publishing to nonexisting exchange would result in an exception.
        # This operation, just like declaring a queue, is idempotent.
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='fanout')

        # We create event message. It will contain timestamp and randomly chosen event type.
        event = {
            'ts': time(),
            'event_type': random.choice(('INFO', 'ALERT', 'ERROR'))
        }

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key='',        # Fanout exchanges ignore routing keys
            body=json.dumps(event)
        )


if __name__ == '__main__':
    main()
