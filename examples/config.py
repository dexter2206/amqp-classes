"""Common module with connection parameters."""
import pika

HOST = 'localhost'
PORT = 5672

CONN_PARAMETERS = pika.ConnectionParameters(host=HOST, port=PORT)