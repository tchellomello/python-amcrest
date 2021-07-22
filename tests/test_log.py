"""Test log.py functions."""
import responses
import datetime

from .mocktestcase import MockTestCase


class TestLog(MockTestCase):
    """Tests for log.py."""

    @responses.activate
    def test_log_find(self):
        self.add_init_responses()

        responses.add(
            responses.GET,
            self.format_url('log.cgi', {
                'action': 'startFind',
                'condition.StartTime': '2020-01-02 21:05:33',
                'condition.EndTime': '2020-01-03 22:05:33'}),
            body='token=17\r\n',
            status=200)

        url_next = self.format_url('log.cgi', {
            'action': 'doFind',
            'token': 17,
            'count': 100})

        responses.add(
            responses.GET,
            url_next,
            body='\r\n'.join((
                'found=2',
                'items[0].Detail.Address=192.168.1.2',
                'items[0].Detail.Type=CGI',
                'items[0].Level=0',
                'items[0].Time=2020-01-02 22:05:33',
                'items[0].Type=Login',
                'items[0].User=admin',
                'items[1].Detail.Address=192.168.1.2',
                'items[1].Detail.Type=CGI',
                'items[1].Level=0',
                'items[1].Time=2020-01-02 22:06:33',
                'items[1].Type=Logout',
                'items[1].User=admin',
                '')),
            status=200)

        responses.add(
            responses.GET,
            url_next,
            body='\r\n'.join((
                'found=0',
                '')),
            status=200)

        responses.add(
            responses.GET,
            self.format_url('log.cgi', {
                'action': 'stopFind',
                'token': 17}),
            body='\r\n'.join((
                'OK',
                '')),
            status=200)

        c = self.get_amcrest().camera

        time_start = datetime.datetime(2020, 1, 2, 21, 5, 33)
        time_end = datetime.datetime(2020, 1, 3, 22, 5, 33)
        logs = list(c.log_find(time_start, time_end))
        self.assertEqual(2, len(logs))
