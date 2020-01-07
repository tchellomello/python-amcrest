import responses
import amcrest
from unittest import TestCase

try:
    import urllib.parse
    fn_urlencode = urllib.parse.urlencode
except ImportError:
    import urllib
    fn_urlencode = urllib.urlencode


class MockTestCase(TestCase):
    def get_host(self):
        return 'www.example.com'

    def get_port(self):
        return 80

    def get_root_url(self):
        return 'http://{}:{}'.format(self.get_host(), self.get_port())

    def format_url(self, method, args=None):
        args_str = '?' + fn_urlencode(args) if args and len(args) > 0 else ''
        result = self.get_root_url() + '/cgi-bin/' + method + args_str
        return result

    def add_init_responses(self):
        responses.add(
            responses.GET,
            self.format_url('magicBox.cgi', {
                'action': 'getMachineName'}),
            body='name=AMCTEST_MACHINE',
            status=200)

        responses.add(
            responses.GET,
            self.format_url('magicBox.cgi', {
                'action': 'getSerialNo'}),
            body='sn=AMCTESTSERIALNO',
            status=200)

    def get_amcrest(self):
        return amcrest.AmcrestCamera(
            self.get_host(),
            self.get_port(),
            'admin',
            'test')
