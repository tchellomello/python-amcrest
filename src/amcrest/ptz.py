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

from typing_extensions import Literal

from .http import Http

ActionT = Literal["start", "stop"]


class Ptz(Http):
    @property
    def ptz_config(self) -> str:
        return self._get_config("Ptz")

    @property
    async def async_ptz_config(self) -> str:
        return await self._async_get_config("Ptz")

    @property
    def ptz_auto_movement(self) -> str:
        return self._get_config("PtzAutoMovement")

    @property
    async def async_ptz_auto_movement(self) -> str:
        return await self._async_get_config("PtzAutoMovement")

    def ptz_presets_list(self, *, channel: int = 0) -> str:
        ret = self.command(f"ptz.cgi?action=getPresets&channel={channel}")
        return ret.content.decode()

    async def async_ptz_presets_list(self, *, channel: int = 0) -> str:
        ret = await self.async_command(
            f"ptz.cgi?action=getPresets&channel={channel}"
        )
        return ret.content.decode()

    @property
    def ptz_presets_count(self) -> int:
        return self.get_ptz_presets_count(channel=0)

    @property
    async def async_ptz_presets_count(self) -> int:
        return await self.async_get_ptz_presets_count(channel=0)

    def get_ptz_presets_count(self, *, channel: int = 0) -> int:
        ret = self.ptz_presets_list(channel=channel)
        return ret.count("Name=")

    async def async_get_ptz_presets_count(self, *, channel: int = 0) -> int:
        ret = await self.async_ptz_presets_list(channel=channel)
        return ret.count("Name=")

    def ptz_status(self, *, channel: int = 0) -> str:
        ret = self.command(f"ptz.cgi?action=getStatus&channel={channel}")
        return ret.content.decode()

    async def async_ptz_status(self, *, channel: int = 0) -> str:
        ret = await self.async_command(
            f"ptz.cgi?action=getStatus&channel={channel}"
        )
        return ret.content.decode()

    def ptz_tour_routines_list(self, *, channel: int = 0) -> str:
        ret = self.command(
            f"configManager.cgi?action=getTours&channel={channel}"
        )
        return ret.content.decode()

    async def async_ptz_tour_routines_list(self, *, channel: int = 0) -> str:
        ret = await self.async_command(
            f"configManager.cgi?action=getTours&channel={channel}"
        )
        return ret.content.decode()

    def ptz_control_command(
        self,
        action: ActionT,
        code: str,
        *,
        arg1: str = "0",
        arg2: str = "0",
        arg3: str = "0",
        channel: int = 0,
    ) -> bool:
        ret = self.command(
            f"ptz.cgi?action={action}&channel={channel}&code={code}&"
            f"arg1={arg1}&arg2={arg2}&arg3={arg3}"
        )
        return ret.content.decode().strip() == "OK"

    async def async_ptz_control_command(
        self,
        action: ActionT,
        code: str,
        *,
        arg1: str = "0",
        arg2: str = "0",
        arg3: str = "0",
        channel: int = 0,
    ) -> bool:
        ret = await self.async_command(
            f"ptz.cgi?action={action}&channel={channel}&code={code}&"
            f"arg1={arg1}&arg2={arg2}&arg3={arg3}"
        )
        return ret.content.decode().strip() == "OK"

    def zoom_in(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_zoom_in(self, start: bool, *, channel: int = 0) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number

        The magic of zoom in 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="ZoomTele",
            channel=channel,
        )

    def zoom_out(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_zoom_out(self, start: bool, *, channel: int = 0) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number

        The magic of zoom out 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="ZoomWide",
            channel=channel,
        )

    def move_left(
        self, start: bool, *, channel: int = 0, horizontal_speed: int = 1
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            horizontal_speed    - range 1-8

        The magic of move left 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Left",
            arg2=str(horizontal_speed),
            channel=channel,
        )

    async def async_move_left(
        self, start: bool, *, channel: int = 0, horizontal_speed: int = 1
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            horizontal_speed    - range 1-8

        The magic of move left 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="Left",
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_right(
        self, start: bool, *, channel: int = 0, horizontal_speed: int = 1
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            horizontal_speed    - range 1-8

        The magic of move right 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="Right",
            arg2=str(horizontal_speed),
            channel=channel,
        )

    async def async_move_right(
        self, start: bool, *, channel: int = 0, horizontal_speed: int = 1
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            horizontal_speed    - range 1-8

        The magic of move right 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.5 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="Right",
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_up(
        self, start: bool, *, channel: int = 0, vertical_speed: int = 1
    ) -> bool:
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

    async def async_move_up(
        self, start: bool, *, channel: int = 0, vertical_speed: int = 1
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
            vertical_speed      - range 1-8

        The magic of move up 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="Up",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def move_down(
        self, start: bool, *, channel: int = 0, vertical_speed: int = 1
    ) -> bool:
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

    async def async_move_down(
        self, start: bool, *, channel: int = 0, vertical_speed: int = 1
    ) -> bool:
        """
        The magic of move down 1x, 2x etc. is the timer between the cmd
        'start' and cmd 'stop'. My suggestion for start/stop cmd is 0.2 sec
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="Down",
            arg2=str(vertical_speed),
            channel=channel,
        )

    def position_abs(
        self,
        start: bool,
        *,
        horizontal_angle: int = 0,
        vertical_angle: int = 0,
        channel: int = 0,
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            horizontal_angle    - range 0-360
            vertical_angle      - range 0-360
            channel             - channel number

        Go to an absolute coordinate
        """
        return self.ptz_control_command(
            action="start" if start else "stop",
            code="PositionABS",
            arg1=str(horizontal_angle),
            arg2=str(vertical_angle),
            channel=channel,
        )

    async def async_position_abs(
        self,
        start: bool,
        *,
        horizontal_angle: int = 0,
        vertical_angle: int = 0,
        channel: int = 0,
    ) -> bool:
        """
        Params:
            start               - True to start, False to stop
            horizontal_angle    - range 0-360
            vertical_angle      - range 0-360
            channel             - channel number

        Go to an absolute coordinate
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="PositionABS",
            arg1=str(horizontal_angle),
            arg2=str(vertical_angle),
            channel=channel,
        )

    def focus_near(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_focus_near(self, start: bool, *, channel: int = 0) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="FocusNear",
            channel=channel,
        )

    def focus_far(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_focus_far(self, start: bool, *, channel: int = 0) -> bool:
        """
        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="FocusFar",
            channel=channel,
        )

    def iris_large(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_iris_large(self, start: bool, *, channel: int = 0) -> bool:
        """
        Aperture larger

        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="IrisLarge",
            channel=channel,
        )

    def iris_small(self, start: bool, *, channel: int = 0) -> bool:
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

    async def async_iris_small(self, start: bool, *, channel: int = 0) -> bool:
        """
        Aperture smaller

        Params:
            start               - True to start, False to stop
            channel             - channel number
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="IrisSmall",
            channel=channel,
        )

    def go_to_preset(
        self, *, channel: int = 0, preset_point_number: int = 1
    ) -> bool:
        """
        Params:
            channel             - channel number
            preset_point_number - preset point number
        """
        return self.ptz_control_command(
            action="start",
            code="GotoPreset",
            arg2=str(preset_point_number),
            channel=channel,
        )

    async def async_go_to_preset(
        self, *, channel: int = 0, preset_point_number: int = 1
    ) -> bool:
        """
        Params:
            channel             - channel number
            preset_point_number - preset point number
        """
        return await self.async_ptz_control_command(
            action="start",
            code="GotoPreset",
            arg2=str(preset_point_number),
            channel=channel,
        )

    def set_preset(
        self, *, channel: int = 0, preset_point_number: int = 1
    ) -> bool:
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

    async def async_set_preset(
        self, *, channel: int = 0, preset_point_number: int = 1
    ) -> bool:
        """
        Params:
            channel             - channel number
            preset_point_number - preset point number
        """
        return await self.async_ptz_control_command(
            action="start",
            code="SetPreset",
            arg2=str(preset_point_number),
            channel=channel,
        )

    def tour(
        self,
        start: bool = True,
        *,
        channel: int = 0,
        tour_path_number: int = 1,
    ) -> bool:
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

    async def async_tour(
        self,
        start: bool = True,
        *,
        channel: int = 0,
        tour_path_number: int = 1,
    ) -> bool:
        """
        Params:
            start               - True (StartTour) or False (StopTour)
            channel             - channel number
            tour_path_number    - tour path number
        """
        return await self.async_ptz_control_command(
            action="start",
            code="StartTour" if start else "StopTour",
            arg1=str(tour_path_number),
            channel=channel,
        )

    def move_left_up(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
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

    async def async_move_left_up(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="LeftUp",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_left_down(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
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

    async def async_move_left_down(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="LeftDown",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_right_up(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
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

    async def async_move_right_up(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="RightUp",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_right_down(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
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

    async def async_move_right_down(
        self,
        start: bool,
        *,
        channel: int = 0,
        vertical_speed: int = 1,
        horizontal_speed: int = 1,
    ) -> bool:
        """
        Params:
            start            - True to start, False to stop
            channel          - channel number
            vertical_speed   - range is 1-8
            horizontal_speed - range is 1-8
        """
        return await self.async_ptz_control_command(
            action="start" if start else "stop",
            code="RightDown",
            arg1=str(vertical_speed),
            arg2=str(horizontal_speed),
            channel=channel,
        )

    def move_directly(
        self,
        startpoint_x: int,
        startpoint_y: int,
        endpoint_x: int,
        endpoint_y: int,
        *,
        channel: int = 1,
    ) -> str:
        """

        Three-dimensional orientation. Move to the rectangle with screen
        coordinate [startX, startY], [endX, endY]

        Params:
            channel          - channel index, start with 1
            startX, startY, endX and endY - range is 0-8192
        """
        ret = self.command(
            f"ptzBase.cgi?action=moveDirectly&channel={channel}&"
            f"startPoint[0]={startpoint_x}&startPoint[1]={startpoint_y}&"
            f"endPoint[0]={endpoint_x}&endPoint[1]={endpoint_y}"
        )
        return ret.content.decode()

    async def async_move_directly(
        self,
        startpoint_x: int,
        startpoint_y: int,
        endpoint_x: int,
        endpoint_y: int,
        *,
        channel: int = 1,
    ) -> str:
        """

        Three-dimensional orientation. Move to the rectangle with screen
        coordinate [startX, startY], [endX, endY]

        Params:
            channel          - channel index, start with 1
            startX, startY, endX and endY - range is 0-8192
        """
        ret = await self.async_command(
            f"ptzBase.cgi?action=moveDirectly&channel={channel}&"
            f"startPoint[0]={startpoint_x}&startPoint[1]={startpoint_y}&"
            f"endPoint[0]={endpoint_x}&endPoint[1]={endpoint_y}"
        )
        return ret.content.decode()
