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


class Ptz:

    @property
    def ptz_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=Ptz'
        )
        return ret.content.decode('utf-8')

    @property
    def ptz_auto_movement(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=PtzAutoMovement'
        )
        return ret.content.decode('utf-8')

    def zoom_in(self, action=None, channel=0):
        """
        The magic of zoom in 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=ZoomTele&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def zoom_out(self, action=None, channel=0):
        """
        The magic of zoom out 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=ZoomWide&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def move_left(self, action=None, channel=0, vertical_speed=1):
        """
        The magic of move left 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=Left&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_right(self, action=None, channel=0, vertical_speed=1):
        """
        The magic of move right 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=Right&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_up(self, action=None, channel=0, vertical_speed=1):
        """
        The magic of move up 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=Up&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_down(self, action=None, channel=0, vertical_speed=1):
        """
        The magic of move down 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=Down&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')
