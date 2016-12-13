"""Server."""

import socket
import logging

def main():
    server()


def set_address():
    address = ('127.0.0.1', 5000)
    return address


def set_server():
    server = socket.socket(socket.AF_INET,
                    socket.SOCK_STREAM,
                    socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server


def handle_message(conn, buffer_length):
    message = ''
    message_complete = False
    while not message_complete:
        part = conn.recv(buffer_length)
        message += part.decode('utf8')
        print('message: ', message)
        print('len part: ', len(part))
        print('buffer_length: ', buffer_length)
        if len(part) < buffer_length:
            print('setting message to complete: ')
            message_complete = True
            break
    print('return message: ', message)
    return message

def server():
    """Initiates the server, binds the server to an address defined above,
    listens and accepts new connections."""
    print('entering server')
    buffer_length = 2048
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
        conn.sendall(message.encode('utf8'))
        print('Closing connection for: ', addr)
        print('Still listening...(Control + C to stop server)')
        conn.close()
    print('end: ', message)





            #
            # message = ''
            # message_complete = True
            # while message_complete:
            #         buffer_length = 8
            #         message_complete = False
            #         while not message_complete:
            #             part = conn.recv(buffer_length)
            #     # print(part.decode('utf8'))
            #             message += part.decode('utf8')
            #             print(message)
            #             print(buffer_length)
            #             print(len(part))
            #             if len(part) < buffer_length:
            #                 break
            #                 message_complete = False
        #     conn.sendall(message.encode('utf8'))
        #     conn.close()
        # except KeyboardInterrupt:
        #     server.close()



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
