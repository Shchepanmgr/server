from message import Message, Header, Command
from client import Client
from time import sleep
import threading

_commands = set(item.value for item in Command)


def connection_with_server(_client):
    while True:
        try:
            # Try to send message from queue
            if len(_client.queue_send) > 0:
                _client.log('Sending command to server...')
                msg = _client.queue_send.pop(0)
                _client.send_message(msg)

            # Try to process message from queue
            if len(_client.queue_receive) > 0:
                msg = _client.queue_receive.pop(0)

                if msg.header == Header.IDLE:
                    _client.log('Remote Client not connected!')

                if msg.header == Header.RESPONSE:
                    _handle_response(msg, _client.log)

        except ConnectionError:
            _client.connected_to_server = False
            _client.log('Connection with server failed!')

        sleep(0.5)


def _handle_response(msg, log):
    log(f'Response from command: {msg.command.name}')

    if isinstance(msg.payload, Exception):
        log('Exception occured!')
        log(msg.payload)
        return

    if msg.command in [Command.UPLOAD_FILE, Command.UPLOAD_FOLDER]:
        file_name = msg.payload[0] + ('.zip' if msg.command == Command.UPLOAD_FOLDER else '')
        with open(file_name, 'wb') as file:
            file.write(msg.payload[1])
        log(f"File saved as: {file_name}")

    else:
        if isinstance(msg.payload, str):
            print(msg.payload)


if __name__ == "__main__":
    # _client = Client('Local Client', '127.0.0.1', 55554)
    _client = Client('Local Client', '192.168.1.10', 502)

    # _command_thread = threading.Thread(target=command_thread, args=[_client])
    # _command_thread.start()

    # connection_with_server(_client)
    while not _client.connected_to_server:
        pass

    _client.send_message(Message(20))

    print("sent")