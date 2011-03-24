import os

from aspen.configuration import Configuration
from aspen.http import Request
from aspen.tests.fsfix import attach_teardown, mk
from aspen.website import Website
from diesel.protocols.http import HttpHeaders, HttpRequest


def DieselReq():
    diesel_request = HttpRequest('GET', '/', 'HTTP/1.1')
    diesel_request.headers = HttpHeaders(Host='localhost') # else 400 in hydrate
    return diesel_request


def test_basic():
    website = Website(Configuration([]))
    expected = os.getcwd()
    actual = website.root
    assert actual == expected, actual

def test_normal_response_is_returned():
    mk(('index.html', "Greetings, program!"))
    website = Website(Configuration(['fsfix']))
    response = website.handle(Request.from_diesel(DieselReq()))
    expected = '\r\n'.join("""\
HTTP/1.1
Content-Length: 19
Content-Type: text/html; charset=UTF-8

Greetings, program!
""".splitlines())
    actual = response._to_http('1.1')
    assert actual == expected, actual


attach_teardown(globals())