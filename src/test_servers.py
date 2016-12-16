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
    proper_get_request = 'GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
    assert parse_request(proper_get_request) == '/index.html'


def test_parse_request_exeption_wrong_method():
    """Test parse_request raises ValueError exception when wrong method."""
    from server import parse_request
    bad_get_request = 'POST /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
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


# resolve_uri

def test_resolve_uri_input_dir_is_html():
    """Test resolve_uri with directory path returns html."""
    from server import resolve_uri
    output = resolve_uri('/webroot').split('\r\n')
    assert output[3][-7:] == '</html>'
    assert output[3][:15] == '<!DOCTYPE html>'


def test_resolve_uri_input_dir_has_correct_listing():
    """Test that directory inputed returns the correct listing."""
    from server import resolve_uri
    output = resolve_uri('/webroot').split('\r\n')
    assert 'a_web_page.html' in output[3]
    assert 'make_time.py' in output[3]
    assert 'sample.txt' in output[3]
    assert '/images' in output[3]


def test_resolve_uri_input_file_text():
    """Test resolve_uri with file path returns file (txt)."""
    from server import resolve_uri
    output = resolve_uri('sample.txt').split('\r\n')
    correct_ouput = u'This is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n'
    assert output[3] == correct_ouput


def test_resolve_uri_input_file_html():
    """Test resolve_uri with file path returns file (HTML)."""
    from server import resolve_uri
    output = resolve_uri('a_web_page.html').split('\r\n')
    assert output[3][-7:] == '</html>'
    assert output[3][:15] == '<!DOCTYPE html>'


def test_resolve_uri_correct_intial_line_200():
    """Test that outputs correct intial line (HTTP/1.1 200 OK)."""
    from server import resolve_uri
    output = resolve_uri('sample.txt').split('\r\n')
    assert output[0] == 'HTTP/1.1 200 OK'


def test_resolve_uri_correct_inial_line_404():
    """Test that output correct intial line (HTTP/1.1 404 Not Found)."""
    from server import resolve_uri
    output = resolve_uri('').split('\r\n')
    assert output[0] == 'HTTP/1.1 404 Not Found'


def test_resolve_uri_correct_content_type_txt():
    """Test that content-type is text/plain."""
    from server import resolve_uri
    output = resolve_uri('sample.txt').split('\r\n')
    assert output[1] == 'Content-Type: text/plain'


def test_resolve_uri_correct_content_type_html():
    """Test that content-type is text/html."""
    from server import resolve_uri
    output = resolve_uri('a_web_page.html').split('\r\n')
    assert output[1] == 'Content-Type: text/html'


def test_resolve_uri_correct_content_type_png():
    """Test that content-type is image/png."""
    from server import resolve_uri
    output = resolve_uri('images/sample_1.png').split('\r\n')
    assert output[1] == 'Content-Type: image/png'


def test_resolve_uri_correct_content_type_jpeg():
    """Test that content-type is image/jpeg."""
    from server import resolve_uri
    output = resolve_uri('images/Sample_Scene_Balls.jpg').split('\r\n')
    assert output[1] == 'Content-Type: image/jpeg'


def test_resolve_uri_correct_content_type_py():
    """Test that content-type is text/py."""
    from server import resolve_uri
    output = resolve_uri('images/Sample_Scene_Balls.jpg').split('\r\n')
    assert output[1] == 'Content-Type: text/py'


def test_resolve_uri_correct_content_length_jpeg():
    """Test that content-length is 15138 bytes in images/JPEG_example.jpg."""
    from server import resolve_uri
    output = resolve_uri('images/JPEG_example.jpg').split('\r\n')
    assert output[2] == 'Content-Length: 15138'


def test_resolve_uri_correct_content_length_png():
    """Test that content-length is 8760 bytes in images/sample_1.png."""
    from server import resolve_uri
    output = resolve_uri('images/sample_1.png').split('\r\n')
    assert output[2] == 'Content-Length: 8760'


def test_resolve_uri_correct_content_length_txt():
    """Test that content-length is 95 bytes in sample.txt."""
    from server import resolve_uri
    output = resolve_uri('sample.txt').split('\r\n')
    assert output[2] == 'Content-Length: 95'


def test_resolve_uri_correct_content_length_html():
    """Test that content-length is 125 bytes in a_web_page.html."""
    from server import resolve_uri
    output = resolve_uri('a_web_page.html').split('\r\n')
    assert output[2] == 'Content-Length: 125'


def test_resolve_uri_correct_content_length_py():
    """Test that content-length is 278 bytes in make_time.py."""
    from server import resolve_uri
    output = resolve_uri('make_time.py').split('\r\n')
    assert output[2] == 'Content-Length: 278'
