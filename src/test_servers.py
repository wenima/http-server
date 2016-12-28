# encoding: utf-8
"""Tests for client."""


import pytest
import sys


if sys.version[0] == '3':
    word = '¥mes¢sage'
    special_char_8 = "1234567¥"
else:
    word = '¥mes¢sage'.decode('utf8')
    special_char_8 = "1234567¥".decode('utf8')


MESSAGES = [
    ['', ''],
    ['¥mes¢sage', word],
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


def test_server_response_error():
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error().split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] + response_split[4] == 'InternalServerError'
    assert response_error()[-2:] == '\r\n'


def test_client_special_char_with_buffer_length():
    """Test that unicode character can straddle the edge buffer length (8)."""
    from client import client
    message_split = client("1234567¥").split('\r\n')
    assert message_split[3] == special_char_8


def test_client_correct_response_error():
    """Test that client receives correct response error."""
    from client import client
    message_split = client("error").split('\r\n')
    response_split = message_split[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] + response_split[4] == 'InternalServerError'


def test_client_correct_response_ok():
    """Test that client receives correct response ok."""
    from client import client
    message_split = client("hello").split('\r\n')
    response_split = message_split[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '200'
    assert response_split[2] == 'OK'
