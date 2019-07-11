"""Example 02: producer part.

Synopsis: running this script will publish several messages to ex_02 queue (via default exchange)
The messages are meant to be consumed by worker implemented in worker.py.
"""
from examples.config import CONN_PARAMETERS
import pika

QUEUE_NAME = 'ex_02'  # Queue to which "tasks" will arrive

# Tasks are just strings. Workers will simulate O(n) operation on those strings by slepping some time proportional
# to string's length.
TASKS = ['example long task', 'x', 'abc', 'foo', 'bar', 'y']


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # We declare our queue as durable, which means that it should survive broker restarts.
        # Not every queue needs to be durable, but it is somehow desirable for queues holding tasks that
        # need to be executed.
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # Iterate over tasks and publish each one of them. We use delivery_mode=2 to make them persistent.
        for task in TASKS:
            channel.basic_publish(
                exchange='',
                routing_key=QUEUE_NAME,
                body=task,
                properties=pika.BasicProperties(delivery_mode=2)
            )


if __name__ == '__main__':
    main()
