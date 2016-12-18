# encoding: utf-8
"""Tests for client."""


import pytest

# MESSAGES = [
#     ['', ''],
#     ['¥mes¢sage', '¥mes¢sage'],
#     ['message', 'message'],
#     ['qwertyuiopasdfgh', 'qwertyuiopasdfgh'],
#     ['qwertyui', 'qwertyui']
# ]


# @pytest.mark.parametrize('message, output', MESSAGES)
# def test_client(message, output):
#     """Test client to returns same messages it got."""
#     from client import client
#     split_message = client(message).split('\r\n')
#     assert split_message[-2] == output

def test_client():
    """Test client to returns 200 ok response."""
    from client import client
    split_message = client('GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n').split('\r\n')
    assert split_message[0] == 'HTTP/1.1 200 OK'


def test_server_response_ok():
    """Test that the OK response is fully-formed proper response."""
    from server import response_ok
    full_response = response_ok().split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '200'
    assert response_split[2] == 'OK'
    assert response_ok()[-2:] == '\r\n'


def test_server_response_error_500():
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error(500).split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] + response_split[4] == 'InternalServerError'
    assert response_error(500)[-2:] == '\r\n'


def test_server_response_error_404():
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error(404).split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '404'
    assert response_split[2] + response_split[3] == 'NotFound'
    assert response_error(404)[-2:] == '\r\n'


def test_parse_request():
    """Test parse_request returns URI."""
    from server import parse_request
    proper_get_request = 'GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
    assert parse_request(proper_get_request) == '/index.html'


def test_parse_request_exeption_wrong_method():
    """Test parse_request raises ValueError exception when wrong method."""
    from server import parse_request
    bad_get_request = 'POST /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
    with pytest.raises(ValueError, message="405: ('Method Not Allowed'"):
        parse_request(bad_get_request)


def test_parse_request_exeption_wrong_version():
    """Test parse_request raises ValueError exception when wrong version."""
    from server import parse_request
    bad_get_request = 'GET /index.html HTTP/1.5\r\nHost: 127.0.0.1\r\n'
    with pytest.raises(ValueError, message="505: ('HTTP Version Not Supported', 'Cannot fulfill request.')"):
        parse_request(bad_get_request)


def test_parse_request_exeption_wrong_host():
    """Test parse_request raises ValueError exception."""
    from server import parse_request
    bad_get_request = 'GET /index.html HTTP/1.1\r\nHost: www.ht.com\r\n'
    with pytest.raises(ValueError, message="400: ('Bad Request','Bad request syntax or unsupported method')"):
        parse_request(bad_get_request)
