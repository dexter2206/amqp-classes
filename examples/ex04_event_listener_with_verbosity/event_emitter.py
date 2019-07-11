"""Example 04: Event emitter with verbosity support.

Synopsis: this example extends 03 with routing of messages. The idea is as follows: events are published
to the ex_04_events exchange with given routing key equal to event_type. By creating appropriate bindings
listeners should be able to listen to the events of only given type.
"""
from time import time
import json
import random
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_04_events'  # Exchange to which events will be published


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # This time we use direct exchange.
        # The direct exchange passes messages to the queues whose bindings match the routing key.
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='direct')

        # We create event message. It will contain timestamp and randomly chosen event type.
        event = {
            'ts': time(),
            'event_type': random.choice(('INFO', 'ALERT', 'ERROR'))
        }

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=event['event_type'],  # This time the routing key will not be ignored
            body=json.dumps(event)
        )


if __name__ == '__main__':
    main()
