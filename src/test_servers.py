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


RESPONSE_ERROR = [
    [201, 'Created'],
    [202, 'Accepted'],
    [203, 'Non-Authoritative Information'],
    [204, 'No Content'],
    [205, 'Reset Content'],
    [206, 'Partial Content'],
    [400, 'Bad Request'],
    [401, 'Unauthorized'],
    [402, 'Payment Required'],
    [403, 'Forbidden'],
    [404, 'Not Found'],
    [405, 'Method Not Allowed'],
    [406, 'Not Acceptable'],
    [407, 'Proxy Authentication Required'],
    [408, 'Request Timeout'],
    [409, 'Conflict'],
    [410, 'Gone'],
    [411, 'Length Required'],
    [412, 'Precondition Failed'],
    [413, 'Request Entity Too Large'],
    [414, 'Request-URI Too Long'],
    [415, 'Unsupported Media Type'],
    [416, 'Requested Range Not Satisfiable'],
    [417, 'Expectation Failed'],
    [100, 'Continue'],
    [101, 'Switching Protocols'],
    [300, 'Multiple Choices'],
    [301, 'Moved Permanently'],
    [302, 'Found'],
    [303, 'See Other'],
    [304, 'Not Modified'],
    [305, 'Use Proxy'],
    [307, 'Temporary Redirect'],
    [500, 'Internal Server Error'],
    [501, 'Not Implemented'],
    [502, 'Bad Gateway'],
    [503, 'Service Unavailable'],
    [504, 'Gateway Timeout'],
    [505, 'HTTP Version Not Supported']
]


@pytest.fixture
def parse_request_fixture():
    """Fixture for parse_request."""
    from server import parse_request
    return parse_request


@pytest.fixture
def parse_resolve_uri():
    """Fixture for resolve_uri."""
    from server import resolve_uri
    return resolve_uri


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


@pytest.mark.parametrize('code, code_str, ', RESPONSE_ERROR)
def test_server_response_error(code, code_str):
    """Test that the ERROR response is fully-formed proper response."""
    from server import response_error
    full_response = response_error(code).split('\r\n')
    response_split = full_response[0].split()
    print(full_response)
    assert response_split[0][:-4] == 'HTTP'
    assert response_split[1] == str(code)
    del response_split[0], response_split[0]
    assert ' '.join(response_split) == code_str
    assert response_error(500)[-2:] == '\r\n'


def test_parse_request(parse_request_fixture):
    """Test parse_request returns URI."""
    proper_get_request = 'GET /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
    assert parse_request_fixture(proper_get_request) == '/index.html'


def test_parse_request_exeption_wrong_method(parse_request_fixture):
    """Test parse_request raises ValueError exception when wrong method."""
    bad_get_request = 'POST /index.html HTTP/1.1\r\nHost: 127.0.0.1\r\n'
    with pytest.raises(ValueError, message="405: ('Method Not Allowed'"):
        parse_request_fixture(bad_get_request)


def test_parse_request_exeption_wrong_version(parse_request_fixture):
    """Test parse_request raises ValueError exception when wrong version."""
    bad_get_request = 'GET /index.html HTTP/1.5\r\nHost: 127.0.0.1\r\n'
    with pytest.raises(ValueError, message="505: ('HTTP Version Not Supported', 'Cannot fulfill request.')"):
        parse_request_fixture(bad_get_request)


def test_parse_request_exeption_wrong_host(parse_request_fixture):
    """Test parse_request raises ValueError exception."""
    bad_get_request = 'GET /index.html HTTP/1.1\r\nHost: www.ht.com\r\n'
    with pytest.raises(ValueError, message="400: ('Bad Request','Bad request syntax or unsupported method')"):
        parse_request_fixture(bad_get_request)

# resolve_uri tests


def test_resolve_uri_input_dir_is_html(parse_resolve_uri):
    """Test resolve_uri with directory path returns html."""
    output = parse_resolve_uri('/webroot').split('\r\n')
    assert output[3][-7:] == '</html>'
    assert output[3][:15] == '<!DOCTYPE html>'


def test_resolve_uri_input_dir_has_correct_listing(parse_resolve_uri):
    """Test that directory inputed returns the correct listing."""
    output = parse_resolve_uri('/webroot').split('\r\n')
    assert 'a_web_page.html' in output[3]
    assert 'make_time.py' in output[3]
    assert 'sample.txt' in output[3]
    assert '/images' in output[3]


def test_resolve_uri_input_file_text(parse_resolve_uri):
    """Test resolve_uri with file path returns file (txt)."""
    output = parse_resolve_uri('sample.txt').split('\r\n')
    correct_ouput = u'This is a very simple text file.\nJust to show that we can serve it up.\nIt is three lines long.\n'
    assert output[3] == correct_ouput


def test_resolve_uri_input_file_html(parse_resolve_uri):
    """Test resolve_uri with file path returns file (HTML)."""
    output = parse_resolve_uri('a_web_page.html').split('\r\n')
    assert output[3][-7:] == '</html>'
    assert output[3][:15] == '<!DOCTYPE html>'


def test_resolve_uri_correct_intial_line_200(parse_resolve_uri):
    """Test that outputs correct intial line (HTTP/1.1 200 OK)."""
    output = parse_resolve_uri('sample.txt').split('\r\n')
    assert output[0] == 'HTTP/1.1 200 OK'


def test_resolve_uri_correct_inial_line_404(parse_resolve_uri):
    """Test that output correct intial line (HTTP/1.1 404 Not Found)."""
    output = parse_resolve_uri('').split('\r\n')
    assert output[0] == 'HTTP/1.1 404 Not Found'


def test_resolve_uri_correct_content_type_txt(parse_resolve_uri):
    """Test that content-type is text/plain."""
    output = parse_resolve_uri('sample.txt').split('\r\n')
    assert output[1] == 'Content-Type: text/plain'


def test_resolve_uri_correct_content_type_html(parse_resolve_uri):
    """Test that content-type is text/html."""
    output = parse_resolve_uri('a_web_page.html').split('\r\n')
    assert output[1] == 'Content-Type: text/html'


def test_resolve_uri_correct_content_type_png(parse_resolve_uri):
    """Test that content-type is image/png."""
    output = parse_resolve_uri('images/sample_1.png').split('\r\n')
    assert output[1] == 'Content-Type: image/png'


def test_resolve_uri_correct_content_type_jpeg(parse_resolve_uri):
    """Test that content-type is image/jpeg."""
    output = parse_resolve_uri('images/Sample_Scene_Balls.jpg').split('\r\n')
    assert output[1] == 'Content-Type: image/jpeg'


def test_resolve_uri_correct_content_type_py(parse_resolve_uri):
    """Test that content-type is text/py."""
    output = parse_resolve_uri('images/Sample_Scene_Balls.jpg').split('\r\n')
    assert output[1] == 'Content-Type: text/py'


def test_resolve_uri_correct_content_length_jpeg(parse_resolve_uri):
    """Test that content-length is 15138 bytes in images/JPEG_example.jpg."""
    output = parse_resolve_uri('images/JPEG_example.jpg').split('\r\n')
    assert output[2] == 'Content-Length: 15138'


def test_resolve_uri_correct_content_length_png(parse_resolve_uri):
    """Test that content-length is 8760 bytes in images/sample_1.png."""
    output = parse_resolve_uri('images/sample_1.png').split('\r\n')
    assert output[2] == 'Content-Length: 8760'


def test_resolve_uri_correct_content_length_txt(parse_resolve_uri):
    """Test that content-length is 95 bytes in sample.txt."""
    output = parse_resolve_uri('sample.txt').split('\r\n')
    assert output[2] == 'Content-Length: 95'


def test_resolve_uri_correct_content_length_html(parse_resolve_uri):
    """Test that content-length is 125 bytes in a_web_page.html."""
    output = parse_resolve_uri('a_web_page.html').split('\r\n')
    assert output[2] == 'Content-Length: 125'


def test_resolve_uri_correct_content_length_py(parse_resolve_uri):
    """Test that content-length is 278 bytes in make_time.py."""
    output = parse_resolve_uri('make_time.py').split('\r\n')
    assert output[2] == 'Content-Length: 278'
