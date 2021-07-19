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
    def __get_config(self, config_name: str) -> str:
        ret = self.command(
            f"configManager.cgi?action=getConfig&name={config_name}"
        )
        return ret.content.decode()

    @property
    def motion_detection(self) -> str:
        return self.__get_config("MotionDetect")

    @motion_detection.setter
    def motion_detection(self, opt: bool) -> bool:
        return self.set_motion_detection(opt)

    @motion_detection.setter  # type: ignore[attr-defined]
    def motion_recording(self, opt: bool) -> bool:
        return self.set_motion_recording(opt)

    def is_motion_detector_on(self, *, channel: int = 0) -> bool:
        ret = self.motion_detection
        status = [pretty(s) for s in ret.split() if ".Enable=" in s][channel]
        return str2bool(status)  # pylint: disable=no-value-for-parameter

    def is_record_on_motion_detection(self, *, channel: int = 0) -> bool:
        ret = self.motion_detection
        status = [pretty(s) for s in ret.split() if ".RecordEnable=" in s][
            channel
        ]
        return str2bool(status)  # pylint: disable=no-value-for-parameter

    def set_motion_detection(self, opt: bool, *, channel: int = 0) -> bool:
        value = "true" if opt else "false"
        ret = self.command(
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
