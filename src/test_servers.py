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
    """Test returns messages shorter than one buffer in length."""
    from client import client
    assert client(message) == output
