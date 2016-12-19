"""Concurrent server that runs of server module."""


from server import response_ok, response_error, parse_request

from gevent.server import StreamServer

from gevent.monkey import patch_all


buffer_length = 1024


def server(socket, address):
    """Concurrent server."""
    while True:
        try:
            message = b''
            message_complete = False
            while not message_complete:
                part = socket.recv(buffer_length)
                message += part
                print('Receiving message from client...')
                print('consuming: ', len(part))
                print(message.decode('utf8'))
                if len(part) < buffer_length or part[-2:] == b'\r\n':
                    print('setting message to complete: ')
                    message_complete = True
                    break
                else:
                    print('Hold on, there is more...Receiving...')
            print('parsing request...')
            try:
                parse_request(message.decode('utf8'))
            except ValueError as e:
                return response_error(*e.args)
            else:
                print('Request OK')
                socket.sendall(response_ok().encode('utf8'))
        except KeyboardInterrupt:
            print('Closing Server!!')
            break
        socket.close()


if __name__ == '__main__':
    patch_all()
    server = StreamServer(('127.0.0.1', 5000), server)
    print("Starting concurrency server now... ")
    server.serve_forever()
