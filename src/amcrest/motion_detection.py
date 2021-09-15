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

from amcrest.http import Http
from amcrest.utils import pretty, str2bool


class MotionDetection(Http):
    @property
    def motion_detection(self) -> str:
        return self._get_config("MotionDetect")

    @motion_detection.setter
    def motion_detection(self, opt: bool) -> bool:
        return self.set_motion_detection(opt)

    @motion_detection.setter  # type: ignore[attr-defined]
    def motion_recording(self, opt: bool) -> bool:
        return self.set_motion_recording(opt)

    @property
    async def async_motion_detection(self) -> str:
        return await self._async_get_config("MotionDetect")

    def is_motion_detector_on(self, *, channel: int = 0) -> bool:
        ret = self.motion_detection
        status = [pretty(s) for s in ret.split() if ".Enable=" in s][channel]
        return str2bool(status)

    async def async_is_motion_detector_on(self, *, channel: int = 0) -> bool:
        ret = await self.async_motion_detection
        status = [pretty(s) for s in ret.split() if ".Enable=" in s][channel]
        return str2bool(status)

    def is_record_on_motion_detection(self, *, channel: int = 0) -> bool:
        ret = self.motion_detection
        status = [pretty(s) for s in ret.split() if ".RecordEnable=" in s][
            channel
        ]
        return str2bool(status)

    async def async_is_record_on_motion_detection(
        self, *, channel: int = 0
    ) -> bool:
        ret = await self.async_motion_detection
        status = [pretty(s) for s in ret.split() if ".RecordEnable=" in s][
            channel
        ]
        return str2bool(status)

    def set_motion_detection(self, opt: bool, *, channel: int = 0) -> bool:
        value = "true" if opt else "false"
        ret = self.command(
            "configManager.cgi?action="
            f"setConfig&MotionDetect[{channel}].Enable={value}"
        )
        return "ok" in ret.content.decode().lower()

    async def async_set_motion_detection(
        self, opt: bool, *, channel: int = 0
    ) -> bool:
        value = "true" if opt else "false"
        ret = await self.async_command(
            "configManager.cgi?action="
            f"setConfig&MotionDetect[{channel}].Enable={value}"
        )
        return "ok" in ret.content.decode().lower()

    def set_motion_recording(self, opt: bool, *, channel: int = 0) -> bool:
        value = "true" if opt else "false"
        ret = self.command(
            "configManager.cgi?action="
            f"setConfig&MotionDetect[{channel}].EventHandler."
            f"RecordEnable={value}"
        )
        return "ok" in ret.content.decode().lower()

    async def async_set_motion_recording(
        self, opt: bool, *, channel: int = 0
    ) -> bool:
        value = "true" if opt else "false"
        ret = await self.async_command(
            "configManager.cgi?action="
            f"setConfig&MotionDetect[{channel}].EventHandler."
            f"RecordEnable={value}"
        )
        return "ok" in ret.content.decode().lower()
