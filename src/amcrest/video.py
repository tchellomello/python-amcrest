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

from typing import List

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
    def encode_media(self) -> str:
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

    def video_in_option(
        self, param: str, *, profile: str = "Day"
    ) -> List[str]:
        """
        Return video input option.

        Params:
            param - parameter, such as 'DayNightColor'
            profile - 'Day', 'Night' or 'Normal'
        """
        if profile == "Day":
            field = param
        else:
            field = f"{profile}Options.{param}"
        return [
            utils.pretty(opt)
            for opt in self.video_in_options.split()
            if f"].{field}=" in opt
        ]

    def set_video_in_option(
        self, param: str, value: str, *, profile: str = "Day", channel: int = 0
    ) -> str:
        if profile == "Day":
            field = param
        else:
            field = f"{profile}Options.{param}"
        ret = self.command(
            "configManager.cgi?action=setConfig"
            f"&VideoInOptions[{channel}].{field}={value}"
        )
        return ret.content.decode()

    def get_day_night_color(self, channel: int) -> int:
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        values = [int(x) for x in self.video_in_option("DayNightColor")]
        return values[channel]

    def set_day_night_color(self, value: int, channel: int) -> str:
        return self.set_video_in_option(
            "DayNightColor", str(value), channel=channel
        )

    def is_smart_ir_on(self, channel: int) -> bool:
        """Return if SmartIR is on."""
        return self.video_in_option("InfraRed")[channel] == "false"

    def set_smart_ir(self, value: bool, channel: int) -> str:
        # It's not clear why from the HTTP API SDK doc, but setting InfraRed
        # to false sets the Night Vision Mode to SmartIR, whereas setting it
        # to true sets the Night Vision Mode to OFF. Night Vision Mode has a
        # third setting of Manual, but that must be selected some other way
        # via the HTTP API.
        str_value = "false" if value else "true"
        return self.set_video_in_option("InfraRed", str_value, channel=channel)

    def is_video_enabled(
        self, channel: int, *, stream: str = "Main", stream_type: int = 0
    ) -> bool:
        """Return if given video stream enabled.

        The stream should be either "Main" or "Extra".  For the main stream,
        the stream type selects if it should read regular (0), motion detection
        (1), alarm (2), or emergency (3) encode settings.  For the extra
        stream, the stream type selects if it should read extra stream 1 (0) or
        extra stream 2 (0) settings.
        """
        is_enabled = utils.extract_audio_video_enabled(
            f"{stream}Format[{stream_type}].Video", self.encode_media
        )
        return is_enabled[channel]

    def set_video_enabled(self, enable: bool, channel: int) -> None:
        self.command(utils.enable_audio_video_cmd("Video", enable, channel))
        self.set_smart_ir(enable, channel)

    @property
    def day_night_color(self) -> int:
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        return self.get_day_night_color(channel=0)

    @day_night_color.setter
    def day_night_color(self, value: int) -> str:
        return self.set_video_in_option("DayNightColor", str(value), channel=0)

    @property
    def smart_ir(self) -> bool:
        """Return if SmartIR is on."""
        return self.is_smart_ir_on(channel=0)

    @smart_ir.setter
    def smart_ir(self, value: bool) -> str:
        return self.set_smart_ir(value, channel=0)

    @property
    def video_enabled(self) -> bool:
        """Return if main video stream enabled."""
        return self.is_video_enabled(channel=0)

    @video_enabled.setter
    def video_enabled(self, enable: bool) -> None:
        self.set_video_enabled(enable, channel=0)

    @property
    def video_out_options(self) -> str:
        ret = self.command("configManager.cgi?action=getConfig&name=VideoOut")
        return ret.content.decode()
