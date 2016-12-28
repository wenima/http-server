# encoding: utf-8
"""Small localtcp/ip server to host connections from local client."""

import socket
import sys
import os
import datetime


address = ('127.0.0.1', 5000)


def response_ok():
    """Return a well formed HTTP 200 OK response."""
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/plain\r\n'
    response += 'Date: ' + datetime.datetime.now().strftime('%a %b %Y %X PST') + '\r\n'
    return response


def response_error():
    """Return a well formed HTTP 500 Internal Server Error response."""
    response = 'HTTP/1.1 500 Internal Server Error\r\n'
    response += 'Content-Type: text/plain\r\n'
    response += 'Date: ' + datetime.datetime.now().strftime('%a %b %Y %X PST') + '\r\n'
    return response


def main():
    """Call server."""
    server()


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
    message = []
    while True:
        part = conn.recv(buffer_length)
        message.append(part)
        print('Receiving message from client...')
        print('consuming: ', len(part))
        if len(part) < buffer_length or part[-2:] == b'\r\n':
            print('setting message to complete: ')
            break
        else:
            print('Hold on, there is more...Receiving...')
    full_message = b''.join(message)
    print('return message: ', full_message)
    if full_message == 'error':
        return response_error()
    else:
        return response_ok().encode('utf8') + full_message


def server():
    """Start the server binds the server to an address listens and accepts."""
    print('entering server')
    buffer_length = 8
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
    except KeyboardInterrupt:
        print('Keyboard interrupted, shutting down server...')
        server.close()
        try:
            sys.exit(0)
        except SystemExit:
            os.exit(0)
