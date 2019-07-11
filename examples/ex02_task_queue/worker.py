"""Example 02: worker part.

Synopsis: this script launches a worker that will consume messages published by producer.py
Since we don't want to bloat our code with some real task, we will simulate task with running time
proportional to length of the message by just sleeping.
"""
from time import sleep
from examples.config import CONN_PARAMETERS
import pika

QUEUE_NAME = 'ex_02'  # Queue to which "tasks" will arrive

# Tasks are just strings. Workers will simulate O(n) operation on those strings by slepping some time proportional
# to string's length.
TASKS = ['example long task', 'x', 'abc', 'foo', 'bar', 'y']


def on_message(channel, method, properties, body):
    task = body.decode('utf-8')
    print(f'Received task "{task}"')
    sleep(len(body))
    print(f'Task {task} completed.')
    # Note that this time we need to manually acknowledge message!
    channel.basic_ack(delivery_tag=method.delivery_tag)


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # We declare our queue as durable, which means that it should survive broker restarts.
        # Not every queue needs to be durable, but it is somehow desirable for queues holding tasks that
        # need to be executed.
        channel.queue_declare(queue=QUEUE_NAME, durable=True)

        # This will enable QoS for our channel. The broker will distribute work to free workers, with maximum of
        # one task scheduled for each worker at the time.
        channel.basic_qos(prefetch_count=1)

        channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_message)
        print('Starting consuming...')

        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            print('Finished consuming.')


if __name__ == '__main__':
    main()
