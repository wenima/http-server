"""Server."""

import socket


def server():
    """Server."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    address = ('127.0.0.1', 5000)
    server.bind(address)
    server.listen(1)
    conn, addr = server.accept()
    message = ''
    while True:
            buffer_length = 8
            message_complete = False
            while not message_complete:
                part = conn.recv(buffer_length)
                message += part.decode('utf8')
                if len(part) < buffer_length:
                    break
    conn.sendall(message.encode('utf8'))
    # conn.close()
    # server.close()

server()

    # try:

    # except KeyboardInterrupt:
