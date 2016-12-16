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


def test_server_response_error():
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error().split('\r\n')
    response_split = full_response[0].split()
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == '500'
    assert response_split[2] + response_split[3] + response_split[4] == 'InternalServerError'
    assert response_error()[-2:] == '\r\n'
