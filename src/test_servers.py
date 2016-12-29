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
    """Test returns messages shorter than one buffer in length."""
    from client import client
    assert client(message)[:-2] == output


def test_client_special_char_with_buffer_length():
    """Test that unicode character can straddle the edge buffer length (8)."""
    from client import client
    assert client("1234567¥")[:-2] == special_char_8
