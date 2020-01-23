# -*- coding: utf-8 -*-
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# vim:sw=4:ts=4:et


class Log(object):

    @property
    def log_clear_all(self):
        ret = self.command(
            'log.cgi?action=clear'
        )
        return ret.content.decode('utf-8')

    def log_show(self, start_time, end_time):
        ret = self.command(
            'Log.backup?action=All&condition.StartTime='
            '{0}&condition.EndTime={1}'.format(start_time, end_time)
        )
        return ret.content.decode('utf-8')

    def log_find_start(self, start_time, end_time):
        ret = self.command(
            'log.cgi?action=startFind'
            '&condition.StartTime={0}&condition.EndTime={1}'
            .format(
                start_time.strftime('%Y-%m-%d %H:%M:%S'),
                end_time.strftime('%Y-%m-%d %H:%M:%S')))

        return ret.content.decode('utf-8')

    def log_find_next(self, token, count=100):
        ret = self.command('log.cgi?action=doFind&token={0}&count={1}'
                           .format(token, count))
        return ret.content.decode('utf-8')

    def log_find_stop(self, token):
        ret = self.command('log.cgi?action=stopFind&token={0}'
                           .format(token))
        return ret.content.decode('utf-8')

    def log_find(self, start_time, end_time):
        token = self.log_find_start(start_time, end_time).strip().split('=')[1]
        to_query = True

        while to_query:
            content = self.log_find_next(token)
            tag, count = (
                list(content.split('\r\n', 1)[0]
                     .split('=')) + [None])[:2]

            to_query = False

            if (tag == 'found') and (int(count) > 0):
                to_query = True

            yield content

        self.log_find_stop(token)
