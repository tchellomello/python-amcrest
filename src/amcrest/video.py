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

from typing import List, Optional, Union

from . import utils
from .http import Http


class Video(Http):
    @property
    def video_max_extra_streams(self) -> int:
        ret = self.command(
            "magicBox.cgi?action=getProductDefinition&name=MaxExtraStream"
        )
        return int(utils.pretty(ret.content.decode()))

    @property
    def video_color_config(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoColor"
        )
        return ret.content.decode()

    @property
    def encode_capability(self) -> str:
        ret = self.command("encode.cgi?action=getCaps")
        return ret.content.decode()

    def encode_config_capability(self, channel: int) -> str:
        ret = self.command(
            f"encode.cgi?action=getConfigCaps&channel={channel}"
        )
        return ret.content.decode()

    @property
    def encode_media_config(self) -> str:
        ret = self.command("configManager.cgi?action=getConfig&name=Encode")
        return ret.content.decode()

    @property
    def encode_region_interested(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoEncodeROI"
        )
        return ret.content.decode()

    @property
    def video_channel_title(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=ChannelTitle"
        )
        return ret.content.decode()

    # pylint: disable=invalid-name
    @property
    def video_input_channels_device_supported(self) -> str:
        ret = self.command("devVideoInput.cgi?action=getCollect")
        return ret.content.decode()

    # pylint: disable=invalid-name
    @property
    def video_output_channels_device_supported(self) -> str:
        ret = self.command("devVideoOutput.cgi?action=getCollect")
        return ret.content.decode()

    # pylint: disable=invalid-name
    @property
    def video_max_remote_input_channels(self) -> str:
        ret = self.command(
            "magicBox.cgi?action=getProductDefinition&name="
            "MaxRemoteInputChannels"
        )
        return ret.content.decode()

    @property
    def video_standard(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoStandard"
        )
        return ret.content.decode()

    @video_standard.setter
    def video_standard(self, std: str) -> str:
        ret = self.command(
            f"configManager.cgi?action=setConfig&VideoStandard={std}"
        )
        return ret.content.decode()

    @property
    def video_widget_config(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoWidget"
        )
        return ret.content.decode()

    def video_input_capability(self, channel: int) -> str:
        ret = self.command(
            f"devVideoInput.cgi?action=getCaps&channel={channel}"
        )
        return ret.content.decode()

    def video_coordinates_current_window(self, channel: int) -> str:
        ret = self.command(
            f"devVideoInput.cgi?action=getCurrentWindow&channel={channel}"
        )
        return ret.content.decode()

    @property
    def video_in_options(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoInOptions"
        )
        return ret.content.decode()

    def video_in_option(self, param: str) -> List[str]:
        """Return video input option.

        Params:
            param - parameter, such as 'DayNightColor'
        """
        return [
            utils.pretty(opt)
            for opt in self.video_in_options.split()
            if f"].{param}=" in opt
        ]

    def set_video_in_option(self, param, value, *, channel: int) -> str:
        ret = self.command(
            "configManager.cgi?action=setConfig&"
            f"VideoInOptions[{channel}].{param}={value}"
        )
        return ret.content.decode()

    def day_night_color(
        self, *, channel: Optional[int] = None
    ) -> Union[int, List[int]]:
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        ret = self.video_in_option("DayNightColor")
        color_modes = [int(x) for x in ret]

        if channel is None:
            return color_modes
        return color_modes[channel]

    def set_day_night_color(self, value: int, channel: int) -> str:
        return self.set_video_in_option(
            "DayNightColor", value, channel=channel
        )

    def get_smart_ir(
        self, *, channel: Optional[int] = None
    ) -> Union[bool, List[bool]]:
        """Return if SmartIR is on."""
        ret = [value == "false" for value in self.video_in_option("InfraRed")]
        if channel is None:
            return ret
        return ret[channel]

    def set_smart_ir(self, value: bool, channel: int) -> str:
        # It's not clear why from the HTTP API SDK doc, but setting InfraRed
        # to false sets the Night Vision Mode to SmartIR, whereas setting it
        # to true sets the Night Vision Mode to OFF. Night Vision Mode has a
        # third setting of Manual, but that must be selected some other way
        # via the HTTP API.
        return self.set_video_in_option(
            "InfraRed", str(not value).lower(), channel=channel
        )

    @property
    def video_out_options(self) -> str:
        ret = self.command("configManager.cgi?action=getConfig&name=VideoOut")
        return ret.content.decode()

    def is_video_enabled(self, *, channel: int = 0) -> bool:
        """Return if any video stream enabled."""
        is_enabled = utils.extract_audio_video_enabled(
            "Video", self.encode_media_config
        )
        return is_enabled[channel]

    def set_video_enabled(self, enable: bool, *, channel: int = 0) -> None:
        self.command(utils.enable_audio_video_cmd("Video", enable, channel))
        self.smart_ir = enable
