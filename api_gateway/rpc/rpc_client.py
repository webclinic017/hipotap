import pika
import uuid


class RpcInProgressException(Exception):
    pass


class RpcClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._open_channel()
        self.call_in_progress = False

    def _open_connection(self):
        if self.connection is not None and self.connection.is_open():
            return

        credentials = pika.PlainCredentials("guest", "guest")
        parameters = pika.ConnectionParameters("hipotap_broker", 5672, "/", credentials)
        self.connection = pika.BlockingConnection(parameters)

    def _open_channel(self):
        if self.channel is not None and self.channel.is_open:
            return
        self._open_connection()
        self.channel = self.connection.channel()

    def _open_response_queue(self):
        # Open response queue
        queue_info = self.channel.queue_declare("", exclusive=True)
        self.callback_queue = queue_info.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue, on_message_callback=self.on_response
        )
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
        self.call_in_progress = False

    def init_callback(self):
        if self.call_in_progress:
            raise RpcInProgressException()
        self._open_channel()
        self._open_response_queue()

        # Set idenfitier of the request
        self.corr_id = str(uuid.uuid4())
        self.call_in_progress = True

    def __del__(self):
        self.connection.close()
