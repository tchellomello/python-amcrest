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
        ret = self.command("configManager.cgi?action=getConfig&name=Ptz")
        return ret.content.decode("utf-8")

    @property
    def ptz_auto_movement(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=PtzAutoMovement"
        )
        return ret.content.decode("utf-8")

    def ptz_presets_list(self, channel=0):
        ret = self.command(
            "ptz.cgi?action=getPresets&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    @property
    def ptz_presets_count(self):
        return self.get_ptz_presets_count(channel=0)

    def get_ptz_presets_count(self, channel=0):
        ret = self.ptz_presets_list(channel=channel)
        return ret.count("Name=")

    def ptz_status(self, channel=0):
        ret = self.command(
            "ptz.cgi?action=getStatus&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    def ptz_tour_routines_list(self, channel=0):
        ret = self.command(
            "configManager.cgi?action=getTours&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    def ptz_control_command(
        self,
        action,
        code,
        arg1="0",
        arg2="0",
        arg3="0",
        channel=0,
    ):
        ret = self.command(
            "ptz.cgi?action={0}&channel={1}&code={2}&arg1={3}"
            "&arg2={4}&arg3={5}".format(
                action, channel, code, arg1, arg2, arg3
            )
        )
        return ret.content.decode("utf-8")

    def zoom_in(self, start, channel=0):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number

        The magic of zoom in 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="ZoomTele",
            channel=channel,
        )

    def zoom_out(self, start, channel=0):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number

        The magic of zoom out 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="ZoomWide",
            channel=channel,
        )

    def move_left(self, start, channel=0, vertical_speed=1):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move left 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Left",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def move_right(self, start, channel=0, vertical_speed=1):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move right 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Right",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def move_up(self, start, channel=0, vertical_speed=1):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move up 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Up",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def move_down(self, start, channel=0, vertical_speed=1):
        """
        The magic of move down 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Down",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def focus_near(self, start, channel=0):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="FocusNear",
            channel=channel,
        )

    def focus_far(self, start, channel=0):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="FocusFar",
            channel=channel,
        )

    def iris_large(self, start, channel=0):
        """
        Aperture larger

        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="IrisLarge",
            channel=channel,
        )

    def iris_small(self, start, channel=0):
        """
        Aperture smaller

        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="IrisSmall",
            channel=channel,
        )

    def go_to_preset(self, channel=0, preset_point_number=1):
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            preset_point_number - preset point number
        """
        return self.ptz_control_command(
            action="start",
            code="GotoPreset",
            arg2=str(preset_point_number),
            channel=channel,
        )

    def set_preset(self, channel=0, preset_point_number=1):
        """
        Params:
            channel             - channel number
            preset_point_number - preset point number
        """
        return self.ptz_control_command(
            action="start",
            code="SetPreset",
            arg2=str(preset_point_number),
            channel=channel,
        )

    def tour(self, start, channel=0, tour_path_number=1):
        """
        Params:
            start               - True (StartTour) or False (StopTour)
            channel             - channel number
            tour_path_number    - tour path number
        """
        return self.ptz_control_command(
            action="start",
            code="StartTour" if start else "StopTour",
            arg1=str(tour_path_number),
            channel=channel,
        )

    def move_left_up(
        self, start, channel=0, vertical_speed=1, horizontal_speed=1
    ):
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="LeftUp",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_left_down(
        self, start, channel=0, vertical_speed=1, horizontal_speed=1
    ):
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="LeftDown",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_right_up(
        self, start, channel=0, vertical_speed=1, horizontal_speed=1
    ):
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="RightUp",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_right_down(
        self, start, channel=0, vertical_speed=1, horizontal_speed=1
    ):
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="RightDown",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_directly(
        self,
        startpoint_x,
        startpoint_y,
        endpoint_x,
        endpoint_y,
        channel=1,
    ):
        """

        Three-dimensional orientation. Move to the rectangle with screen
        coordinate [startX, startY], [endX, endY]

        Params:
            channel          - channel index, start with 1
            startX, startY, endX and endY - range is 0-8192
        """
        ret = self.command(
            "ptzBase.cgi?action=moveDirectly&channel={0}&startPoint[0]={1}"
            "&startPoint[1]={2}&endPoint[0]={3}&endPoint[1]={4}".format(
                channel, startpoint_x, startpoint_y, endpoint_x, endpoint_y
            )
        )
        return ret.content.decode("utf-8")
