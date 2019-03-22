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


class Ptz(object):

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

    def ptz_presets_list(self, channel=0):
        ret = self.command(
            'ptz.cgi?action=getPresets&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    @property
    def ptz_presets_count(self, channel=0):
        ret = self.ptz_presets_list()
        return ret.count("Name=")

    def ptz_status(self, channel=0):
        ret = self.command(
            'ptz.cgi?action=getStatus&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    def ptz_tour_routines_list(self, channel=0):
        ret = self.command(
            'configManager.cgi?action=getTours&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    def ptz_control_command(self, channel=0, action=None, code=None,
                            arg1=None, arg2=None, arg3=None):

        if action is None and code is None and arg1 is None and \
                arg2 is None and arg3 is None:
            raise RuntimeError("code, arg1, arg2, arg3 is required!")

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code={2}&arg1={3}'
            '&arg2={4}&arg3={5}'.format(action, channel, code,
                                        arg1, arg2, arg3)
        )
        return ret.content.decode('utf-8')

    def zoom_in(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number

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
        Params:
            action              - start or stop
            channel             - channel number

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
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

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
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

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
        Params:
            action              - start or stop
            channel             - channel number
            vertical_speed      - range 1-8

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

    def focus_near(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=FocusNear&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def focus_far(self, action=None, channel=0):
        """
        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=FocusFar&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def iris_large(self, action=None, channel=0):
        """
        Aperture larger

        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=IrisLarge&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def iris_small(self, action=None, channel=0):
        """
        Aperture smaller

        Params:
            action              - start or stop
            channel             - channel number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=IrisSmall&arg1=0'
            '&arg2=0&arg3=0'.format(action, channel)
        )
        return ret.content.decode('utf-8')

    def go_to_preset(self, action=None, channel=0, preset_point_number=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            preset_point_number - preset point number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=GotoPreset&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, preset_point_number)
        )
        return ret.content.decode('utf-8')

    def tour(self, action='start', channel=0, start=True, tour_path_number=1):
        """
        Params:
            action              - start or stop
            channel             - channel number
            start               - True (StartTour) or False (StopTour)
            tour_path_number    - tour path number
        """
        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code={2}Tour&arg1={3}'
            '&arg2=0&arg3=0&arg4=0'.format(
                action, channel, 'Start' if start else 'Stop',
                tour_path_number)
        )
        return ret.content.decode('utf-8')

    def move_left_up(self, action=None, channel=0,
                     vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=LeftUp&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_left_down(self, action=None, channel=0,
                       vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=LeftDown&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_right_up(self, action=None, channel=0,
                      vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=RightUp&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_right_down(self, action=None, channel=0,
                        vertical_speed=1, horizontal_speed=1):
        """
        Params:
            action           - start or stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """

        ret = self.command(
            'ptz.cgi?action={0}&channel={1}&code=RightDown&arg1=0'
            '&arg2={2}&arg3=0'.format(action, channel, vertical_speed)
        )
        return ret.content.decode('utf-8')

    def move_directly(self,
                      channel=1, startpoint_x=None, startpoint_y=None,
                      endpoint_x=None, endpoint_y=None):
        """

        Three-dimensional orientation. Move to the rectangle with screen
        coordinate [startX, startY], [endX, endY]

        Params:
            action           - start or stop
            channel          - channel index, start with 1
            startX, startY, endX and endY - range is 0-8192
        """

        if startpoint_x is None or startpoint_y is None or \
           endpoint_x is None or endpoint_y is None:
            raise RuntimeError("Required args, start_point_x, start_point_y"
                               "end_point_x and end_point_y not speficied")

        ret = self.command(
            'ptzBase.cgi?action=moveDirectly&channel={0}&startPoint[0]={1}'
            '&startPoint[1]={2}&endPoint[0]={3}&endPoint[1]={4}'.format(
                channel, startpoint_x, startpoint_y, endpoint_x, endpoint_y)
        )
        return ret.content.decode('utf-8')
