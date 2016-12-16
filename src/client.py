# encoding: utf-8
"""Local TCP/IP client to send/receive messages to local server."""

import socket
import time
import sys


buffer_length = 8


def client(message):
    """Send a message to the local server echos back the same message."""
    infos = socket.getaddrinfo('127.0.0.1', 5000)
    stream_info = [i for i in infos if i[1] == socket.SOCK_STREAM][0]
    client = socket.socket(*stream_info[:3])
    client.connect(stream_info[-1])
    print('sending the following message:',
          message, 'to server at: ',
          socket.gethostbyname('127.0.0.1'))
    if sys.version[0] == '3':
        client.sendall(message.encode('utf8') + b'\r\n')
    else:
        client.sendall(message + b'\r\n')
    reply_complete = False
    # server_message = []
    server_message = b''
    begin = time.time()
    timeout = 2
    time.sleep(0.1)
    while not reply_complete:
        if message and time.time() - begin > timeout:
            break
        elif time.time() - begin > timeout * 2:
            break
        part = client.recv(buffer_length)
        if part:
            server_message += part
            print('Receiving message from server...')
            print(server_message[-1])
            begin = time.time()
            time.sleep(0.1)
        if len(part) < buffer_length:
            break
        else:
            print('Hold on, there is more...Receiving...')
    client.close()
    if sys.version[0] == '3':
        return str(server_message, 'utf8')
    else:
        return str(server_message)


if __name__ == '__main__':
    message = sys.argv[1]
    print(client(message))
