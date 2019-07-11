"""Example 01: basic example of AMQP publisher"""
from examples.config import CONN_PARAMETERS
import pika


def main():
    """Entry point of this script."""
    # Create connection to the broker
    conn = pika.BlockingConnection(CONN_PARAMETERS)

    # Create channel for communication with broker.
    # Remember that channel (not a connection!) is a basic unit of communication with broker.
    channel = conn.channel()

    # Make sure queue exists. Declaring queue is idempotent (i.e. declaring queue multiple times has no effect)*.
    channel.queue_declare(queue='hello_world')

    # Publish message to default exchange. This looks like we are publishing directly to hello_world queue
    # but remember that the exchange is always there. Its just the specific behavior of the default exchange
    # that allows us to make a simplification of publishing to given queue.
    channel.basic_publish(exchange='', routing_key='hello_world', body='Hello World!')

    # Close connection. Note that Blocking connection is a context manager, so we actually could achieve the same
    # by using with-statement.
    conn.close()


if __name__ == '__main__':
    main()
