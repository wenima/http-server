# encoding: utf-8
"""Small localtcp/ip server to host connections from local client."""

import socket
import sys
import os
import email.utils


responses = {
    100: ('Continue', 'Request received, please continue'),
    101: ('Switching Protocols',
          'Switching to new protocol; obey Upgrade header'),

    200: ('OK', 'Request fulfilled, document follows'),
    201: ('Created', 'Document created, URL follows'),
    202: ('Accepted',
          'Request accepted, processing continues off-line'),
    203: ('Non-Authoritative Information', 'Request fulfilled from cache'),
    204: ('No Content', 'Request fulfilled, nothing follows'),
    205: ('Reset Content', 'Clear input form for further input.'),
    206: ('Partial Content', 'Partial content follows.'),

    300: ('Multiple Choices',
          'Object has several resources -- see URI list'),
    301: ('Moved Permanently', 'Object moved permanently -- see URI list'),
    302: ('Found', 'Object moved temporarily -- see URI list'),
    303: ('See Other', 'Object moved -- see Method and URL list'),
    304: ('Not Modified',
          'Document has not changed since given time'),
    305: ('Use Proxy',
          'You must use proxy specified in Location to access this '
          'resource.'),
    307: ('Temporary Redirect',
          'Object moved temporarily -- see URI list'),

    400: ('Bad Request',
          'Bad request syntax or unsupported method'),
    401: ('Unauthorized',
          'No permission -- see authorization schemes'),
    402: ('Payment Required',
          'No payment -- see charging schemes'),
    403: ('Forbidden',
          'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
          'Specified method is invalid for this resource.'),
    406: ('Not Acceptable', 'URI not available in preferred format.'),
    407: ('Proxy Authentication Required', 'You must authenticate with '
          'this proxy before proceeding.'),
    408: ('Request Timeout', 'Request timed out; try again later.'),
    409: ('Conflict', 'Request conflict.'),
    410: ('Gone',
          'URI no longer exists and has been permanently removed.'),
    411: ('Length Required', 'Client must specify Content-Length.'),
    412: ('Precondition Failed', 'Precondition in headers is false.'),
    413: ('Request Entity Too Large', 'Entity is too large.'),
    414: ('Request-URI Too Long', 'URI is too long.'),
    415: ('Unsupported Media Type', 'Entity body in unsupported format.'),
    416: ('Requested Range Not Satisfiable',
          'Cannot satisfy request range.'),
    417: ('Expectation Failed',
          'Expect condition could not be satisfied.'),

    500: ('Internal Server Error', 'Server got itself in trouble'),
    501: ('Not Implemented',
          'Server does not support this operation'),
    502: ('Bad Gateway', 'Invalid responses from another server/proxy.'),
    503: ('Service Unavailable',
          'The server cannot process the request due to a high load'),
    504: ('Gateway Timeout',
          'The gateway server did not receive a timely response'),
    505: ('HTTP Version Not Supported', 'Cannot fulfill request.'),
}


def response_ok():
    """Return a well formed HTTP 200 OK response."""
    response = 'HTTP/1.1 200 OK\r\n'
    response += 'Content-Type: text/plain\r\n'
    response += 'Date: ' + email.utils.formatdate(usegmt=True) + '\r\n'
    return response


def response_error(err_code):
    """Return a well formed Error response."""
    response = 'HTTP/1.1 {0} {1}\r\n'
    response += 'Content-Type: text/plain\r\n'
    response += 'Date: ' + email.utils.formatdate(usegmt=True) + '\r\n'
    return ''.join(response).format(err_code, responses[err_code][0])


def main():
    """Call server."""
    server()


def set_address():
    """Set the adress."""
    address = ('127.0.0.1', 5000)
    return address


def read_address():
    """Read back the current IP adress."""
    return set_address()


def read_hostname():
    """Return host name of server object."""
    server = set_server()
    return server.gethostname()


def set_server():
    """Instantiate the socket object."""
    server = socket.socket(socket.AF_INET,
                           socket.SOCK_STREAM,
                           socket.IPPROTO_TCP)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return server


def parse_request(message):
    """Validate that the request is well-formed if it is return the URI from the request."""
    requestline = message.rstrip('\r\n')
    print(requestline)
    request_split = requestline.split()
    print(request_split)
    command, path, version, host, host_name = request_split
    version_number = version.split('/', 1)[1]
    try:
        if command != 'GET':
            raise ValueError(405)
        elif 'HTTP/' not in version:
            raise ValueError(400)
        elif len(version_number) != 3 or version_number != '1.1':
                raise ValueError(505)
        if host != 'Host:' or host_name != read_address()[0]:
            raise ValueError(400)
    except ValueError:
        raise
    return path


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
        return response_ok().encode('utf8')


def server():
    """Start the server binds the server to an address listens and accepts."""
    print('entering server')
    buffer_length = 1024
    address = set_address()
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
        print('Sending response... ')
        try:
            print(message)
            conn.sendall(message)
        except socket.error as se:
            print('Something went wrong when attempting to send to client:', se)
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
