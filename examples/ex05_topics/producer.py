"""Example 05: producer

Synopsis: this script will produce several messages to the exchange 'ex_05_measurements'
"""
from examples.config import CONN_PARAMETERS
import pika

EXCHANGE = 'ex_05_measurements'  # Exchange to which events will be published


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # In this example we use topic exchange. It works almost like direct exchange, except it allows
        # wildcards (* and #) in the routing key of the binding.
        # The routing key itself should be structured in parts separated with dot (by analogy,
        # routing in this case works like using mqtt topic with / replaced by .).
        channel.exchange_declare(exchange=EXCHANGE, exchange_type='topic')

        channel.basic_publish(exchange=EXCHANGE, routing_key='livingroom.temperature', body='20.2')
        channel.basic_publish(exchange=EXCHANGE, routing_key='livingroom.humidity', body='40%')
        channel.basic_publish(exchange=EXCHANGE, routing_key='bedroom.temperature', body='18.0')
        channel.basic_publish(exchange=EXCHANGE, routing_key='bedroom.humidity', body='60%')


if __name__ == '__main__':
    main()
