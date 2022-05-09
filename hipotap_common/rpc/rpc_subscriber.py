from ..broker import connect_to_brocker


class RpcSubscriber:
    def __init__(self):
        self.connection = None
        self.channel = None
        self._open_channel()

    def _open_connection(self):
        if self.connection is not None and self.connection.is_open():
            return

        self.connection = connect_to_brocker()

    def _open_channel(self):
        if self.channel is not None and self.channel.is_open:
            return
        self._open_connection()
        self.channel = self.connection.channel()

    def subscribe_to_queue(self, queue_name: str, callback: callable):
        # make sure the queue exists
        self.channel.queue_declare(queue_name)

        self.channel.basic_consume(
            queue=queue_name, auto_ack=True, on_message_callback=callback
        )

    def handling_loop(self):
        print(" [*] Staring RPC handling loop. To exit press CTRL+C")
        self.channel.start_consuming()
