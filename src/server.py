# encoding: utf-8
"""Small localtcp/ip server to host connections from local client."""

import socket
import time
import sys
import os


def main():
    """Call server."""
    server()


def set_address():
    """Set the adress."""
    address = ('127.0.0.1', 5000)
    return address


def set_server():
    """Instantiate the socket object."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server


def handle_message(conn, buffer_length):
    """Handle the messages coming into the server."""
    conn.setblocking(1)
    message = b''
    message_complete = False
    while not message_complete:
        part = conn.recv(buffer_length)
        message += part
        print('Receiving message from client...')
        print('consuming: ', len(part))
        time.sleep(0.3)
        print(message[-2:])
        if len(part) < buffer_length or part[-2:] == b'\r\n':
            print('setting message to complete: ')
            message_complete = True
            break
        else:
            print('Hold on, there is more...Receiving...')
    full_message = message
    print('return message: ', full_message)
    return full_message


def server():
    """Start the server binds the server to an address listens and accepts."""
    print('entering server')
    buffer_length = 8
    address = set_address()
    print('address set to: ', address)
    server = set_server()
    server.bind(address)
    server.listen(1)
    print('listening on: ', address)
    while True:
        try:
            conn, addr = server.accept()
            print('Received a connection by: ', addr)
            message = handle_message(conn, buffer_length)
        except KeyboardInterrupt:
            print('Shutting down...')
            print('Goodbye.')
            conn.close()
            server.close()
            exit()
        print('Echoing message back: ')
        conn.sendall(message)
        print('Closing connection for: ', addr)
        print('Still listening...(Control + C to stop server)')
        conn.close()
    print('end: ', message)


if __name__ == '__main__':
    try:
        main()
        # server()
    except KeyboardInterrupt:
        print('Keyboard interrupted, shutting down server...')
        server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
