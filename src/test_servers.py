# encoding: utf-8
"""Tests for client."""


import pytest

MESSAGES = [
    ['', ''],
    ['¥mes¢sage', '¥mes¢sage'],
    ['message', 'message'],
    ['qwertyuiopasdfgh', 'qwertyuiopasdfgh'],
    ['qwertyui', 'qwertyui']
]


@pytest.mark.parametrize('message, output', MESSAGES)
def test_client(message, output):
    """Test client to returns same messages it got."""
    from client import client
    split_message = client(message).split('\r\n')
    assert split_message[-2] == output


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
    full_response = response_error('500', 'Internal Server Error').split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] + response_split[4] == 'InternalServerError'
    assert response_error()[-2:] == '\r\n'


def test_server_response_error_404():
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error('404', 'Not Found').split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] == 'NotFound'
    assert response_error()[-2:] == '\r\n'


def test_parse_request():
    """Test parse_request returns URI."""
    from server import parse_request
    proper_get_request = 'GET /index.html HTTP/1.1\r\nHost: www.example.com\r\n'
    assert parse_request(proper_get_request) == '/index.html'


def test_parse_request_exeption_wrong_method():
    """Test parse_request raises ValueError exception when wrong method."""
    from server import parse_request
    bad_get_request = 'POST /index.html HTTP/1.1\r\nHost: www.example.com\r\n'
    with pytest.raises(ValueError, message="405: ('Method Not Allowed)'"):
        parse_request(bad_get_request)


def test_parse_request_exeption_wrong_path():
    """Test parse_request raises ValueError exception when wrong path."""
    from server import parse_request
    bad_get_request = 'GET /indx.html HTTP/1.1\r\nHost: www.example.com\r\n'
    with pytest.raises(ValueError, message="404: ('Not Found', 'Nothing matches the given URI')"):
        parse_request(bad_get_request)


def test_parse_request_exeption_wrong_version():
    """Test parse_request raises ValueError exception when wrong version."""
    from server import parse_request
    bad_get_request = 'GET /index.html HTTP/1.5\r\nHost: www.example.com\r\n'
    with pytest.raises(ValueError, message="505: ('HTTP Version Not Supported', 'Cannot fulfill request.')"):
        parse_request(bad_get_request)


def test_parse_request_exeption_wrong_host():
    """Test parse_request raises ValueError exception."""
    from server import parse_request
    bad_get_request = 'GET /index.html HTTP/1.1\r\nHost: www.ht.com\r\n'
    with pytest.raises(ValueError, message="400: ('Bad Request','Bad request syntax or unsupported method')"):
        parse_request(bad_get_request)


def test_resolve_uri_input_dir():
    """Test resolve_uri with directory path returns html."""
    from server import resolve_uri
    output = resolve_uri('/webroot').split('\r\n')
    assert output[3][-7:] == '</html>'
    assert output[3][:15] == '<!DOCTYPE html>'


def test_resolve_uri_input_file():
    """Test resolve_uri with file path returns file (txt)."""
    from server import resolve_uri
    output = resolve_uri('/sample.txt').split('\r\n')
    assert output[3] == u'This is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n'
