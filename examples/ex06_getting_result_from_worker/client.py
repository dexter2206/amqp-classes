"""Example 06: client using our worker to get results.

Synopsis: running this script will schedule some tasks for execution by the worker(s), wait
for the results and then print the results.
"""
import uuid
from examples.config import CONN_PARAMETERS
import pika

TASKS_QUEUE_NAME = 'ex_06_tasks'  # Queue to which "tasks" will arrive

FIB_NUMBERS = [30, 5, 2, 3]  # Fibonacci numbers to compute


def create_callback(results_dict):
    """Factory for callback functions. """
    def _on_message(channel, method, properties, body):
        """Callback that will deposit result to the results_dict"""
        results_dict[properties.correlation_id] = int(body)
    return _on_message


def main():
    """Entry point of this script."""

    with pika.BlockingConnection(CONN_PARAMETERS) as conn:

        channel = conn.channel()

        # We declare two queues: one for the tasks, second for the results.
        # The second one is exclusive, as it is specific to our client.
        channel.queue_declare(queue=TASKS_QUEUE_NAME, durable=True)
        reply_queue = channel.queue_declare('', exclusive=True).method.queue

        results_dict = {}
        correlation_map = {}

        channel.basic_consume(
            queue=reply_queue,
            on_message_callback=create_callback(results_dict),
            auto_ack=True
        )

        for number in FIB_NUMBERS:
            correlation_id = str(uuid.uuid4())
            correlation_map[number] = correlation_id

            channel.basic_publish(
                exchange='',
                routing_key=TASKS_QUEUE_NAME,
                properties=pika.BasicProperties(reply_to=reply_queue, correlation_id=correlation_id),
                body=str(number)
            )

        while len(results_dict) != len(FIB_NUMBERS):
            conn.process_data_events()

        for number in FIB_NUMBERS:
            result = results_dict[correlation_map[number]]
            print(f'fibonacci{number} = {result}')


if __name__ == '__main__':
    main()
