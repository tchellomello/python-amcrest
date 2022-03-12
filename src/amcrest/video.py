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
        ret = self._magic_box("getProductDefinition&name=MaxExtraStream")
        return int(utils.pretty(ret))

    @property
    async def async_video_max_extra_streams(self) -> int:
        ret = await self._async_magic_box(
            "getProductDefinition&name=MaxExtraStream"
        )
        return int(utils.pretty(ret))

    @property
    def video_color_config(self) -> str:
        return self._get_config("VideoColor")

    @property
    async def async_video_color_config(self) -> str:
        return await self._async_get_config("VideoColor")

    @property
    def encode_capability(self) -> str:
        ret = self.command("encode.cgi?action=getCaps")
        return ret.content.decode()

    @property
    async def async_encode_capability(self) -> str:
        ret = await self.async_command("encode.cgi?action=getCaps")
        return ret.content.decode()

    def encode_config_capability(self, channel: int) -> str:
        ret = self.command(
            f"encode.cgi?action=getConfigCaps&channel={channel}"
        )
        return ret.content.decode()

    async def async_encode_config_capability(self, channel: int) -> str:
        ret = await self.async_command(
            f"encode.cgi?action=getConfigCaps&channel={channel}"
        )
        return ret.content.decode()

    @property
    def encode_media(self) -> str:
        return self._get_config("Encode")

    @property
    async def async_encode_media(self) -> str:
        return await self._async_get_config("Encode")

    @property
    def encode_region_interested(self) -> str:
        return self._get_config("VideoEncodeROI")

    @property
    async def async_encode_region_interested(self) -> str:
        return await self._async_get_config("VideoEncodeROI")

    @property
    def video_channel_title(self) -> str:
        return self._get_config("ChannelTitle")

    @property
    async def async_video_channel_title(self) -> str:
        return await self._async_get_config("ChannelTitle")

    # pylint: disable=invalid-name
    @property
    def video_input_channels_device_supported(self) -> str:
        ret = self.command("devVideoInput.cgi?action=getCollect")
        return ret.content.decode()

    @property
    async def async_video_input_channels_device_supported(self) -> str:
        ret = await self.async_command("devVideoInput.cgi?action=getCollect")
        return ret.content.decode()

    # pylint: disable=invalid-name
    @property
    def video_output_channels_device_supported(self) -> str:
        ret = self.command("devVideoOutput.cgi?action=getCollect")
        return ret.content.decode()

    @property
    async def async_video_output_channels_device_supported(self) -> str:
        ret = await self.async_command("devVideoOutput.cgi?action=getCollect")
        return ret.content.decode()

    # pylint: disable=invalid-name
    @property
    def video_max_remote_input_channels(self) -> str:
        return self._magic_box(
            "getProductDefinition&name=MaxRemoteInputChannels"
        )

    @property
    async def async_video_max_remote_input_channels(self) -> str:
        return await self._async_magic_box(
            "getProductDefinition&name=MaxRemoteInputChannels"
        )

    @property
    def video_standard(self) -> str:
        return self._get_config("VideoStandard")

    @video_standard.setter
    def video_standard(self, std: str) -> str:
        return self._get_config(f"setConfig&VideoStandard={std}")

    @property
    async def async_video_standard(self) -> str:
        return await self._async_get_config("VideoStandard")

    async def async_set_video_standard(self, std: str) -> str:
        return await self._async_get_config(f"setConfig&VideoStandard={std}")

    @property
    def video_widget_config(self) -> str:
        return self._get_config("VideoWidget")

    @property
    async def async_video_widget_config(self) -> str:
        return await self._async_get_config("VideoWidget")

    def video_input_capability(self, channel: int) -> str:
        ret = self.command(
            f"devVideoInput.cgi?action=getCaps&channel={channel}"
        )
        return ret.content.decode()

    async def async_video_input_capability(self, channel: int) -> str:
        ret = await self.async_command(
            f"devVideoInput.cgi?action=getCaps&channel={channel}"
        )
        return ret.content.decode()

    def video_coordinates_current_window(self, channel: int) -> str:
        ret = self.command(
            f"devVideoInput.cgi?action=getCurrentWindow&channel={channel}"
        )
        return ret.content.decode()

    async def async_video_coordinates_current_window(
        self, channel: int
    ) -> str:
        ret = await self.async_command(
            f"devVideoInput.cgi?action=getCurrentWindow&channel={channel}"
        )
        return ret.content.decode()

    @property
    def video_in_options(self) -> str:
        return self._get_config("VideoInOptions")

    @property
    async def async_video_in_options(self) -> str:
        return await self._async_get_config("VideoInOptions")

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

    async def async_video_in_option(
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
            for opt in (await self.async_video_in_options).split()
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

    async def async_set_video_in_option(
        self, param: str, value: str, *, profile: str = "Day", channel: int = 0
    ) -> str:
        if profile == "Day":
            field = param
        else:
            field = f"{profile}Options.{param}"
        ret = await self.async_command(
            "configManager.cgi?action=setConfig"
            f"&VideoInOptions[{channel}].{field}={value}"
        )
        return ret.content.decode()

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
    async def async_day_night_color(self) -> int:
        """Return Day & Night Color Mode for Day profile."""
        return await self.async_get_day_night_color(channel=0)

    def get_day_night_color(self, channel: int) -> int:
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        values = [int(x) for x in self.video_in_option("DayNightColor")]
        return values[channel]

    async def async_get_day_night_color(self, channel: int) -> int:
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        values = [
            int(x) for x in await self.async_video_in_option("DayNightColor")
        ]
        return values[channel]

    def set_day_night_color(self, value: int, channel: int) -> str:
        return self.set_video_in_option(
            "DayNightColor", str(value), channel=channel
        )

    async def async_set_day_night_color(self, value: int, channel: int) -> str:
        return await self.async_set_video_in_option(
            "DayNightColor", str(value), channel=channel
        )

    @property
    def smart_ir(self) -> bool:
        """Return if SmartIR is on."""
        return self.is_smart_ir_on(channel=0)

    @smart_ir.setter
    def smart_ir(self, value: bool) -> str:
        return self.set_smart_ir(value, channel=0)

    @property
    async def async_smart_ir(self) -> bool:
        """Return if SmartIR is on."""
        return await self.async_is_smart_ir_on(channel=0)

    def is_smart_ir_on(self, channel: int) -> bool:
        """Return if SmartIR is on."""
        return self.video_in_option("InfraRed")[channel] == "false"

    async def async_is_smart_ir_on(self, channel: int) -> bool:
        """Return if SmartIR is on."""
        return (await self.async_video_in_option("InfraRed"))[
            channel
        ] == "false"

    def set_smart_ir(self, value: bool, channel: int) -> str:
        # It's not clear why from the HTTP API SDK doc, but setting InfraRed
        # to false sets the Night Vision Mode to SmartIR, whereas setting it
        # to true sets the Night Vision Mode to OFF. Night Vision Mode has a
        # third setting of Manual, but that must be selected some other way
        # via the HTTP API.
        str_value = "false" if value else "true"
        return self.set_video_in_option("InfraRed", str_value, channel=channel)

    async def async_set_smart_ir(self, value: bool, channel: int) -> str:
        # It's not clear why from the HTTP API SDK doc, but setting InfraRed
        # to false sets the Night Vision Mode to SmartIR, whereas setting it
        # to true sets the Night Vision Mode to OFF. Night Vision Mode has a
        # third setting of Manual, but that must be selected some other way
        # via the HTTP API.
        str_value = "false" if value else "true"
        return await self.async_set_video_in_option(
            "InfraRed", str_value, channel=channel
        )

    @property
    def video_enabled(self) -> bool:
        """Return if main video stream enabled."""
        return self.is_video_enabled(channel=0)

    @video_enabled.setter
    def video_enabled(self, enable: bool) -> None:
        self.set_video_enabled(enable, channel=0)

    @property
    async def async_video_enabled(self) -> bool:
        """Return if main video stream enabled."""
        return await self.async_is_video_enabled(channel=0)

    def is_video_enabled(
        self, channel: int, *, stream: str = "Main", stream_type: int = 0
    ) -> bool:
        """Return if given video stream enabled.

        The stream should be either "Main", "Extra", or "Snap".  For the main
        stream, the stream type selects if it should read regular (0), motion
        detection (1), alarm (2), or emergency (3) encode settings.  The snap
        stream has the same settings for regular, motion detection, and alarm
        stream types.  For the extra stream, the stream type selects which
        stream should be read, and is zero indexed from 0 to 2 for streams 1 to
        3.
        """
        is_enabled = utils.extract_audio_video_enabled(
            f"{stream}Format[{stream_type}].Video", self.encode_media
        )
        return is_enabled[channel]

    async def async_is_video_enabled(
        self, channel: int, *, stream: str = "Main", stream_type: int = 0
    ) -> bool:
        """Return if given video stream enabled."""
        is_enabled = utils.extract_audio_video_enabled(
            f"{stream}Format[{stream_type}].Video",
            await self.async_encode_media,
        )
        return is_enabled[channel]

    def set_video_enabled(
        self, enable: bool, channel: int, *, stream: str = "Main"
    ) -> None:
        self.command(
            utils.enable_audio_video_cmd(
                "Video", enable, channel, stream=stream
            )
        )
        self.set_smart_ir(enable, channel)

    async def async_set_video_enabled(
        self, enable: bool, channel: int, *, stream: str = "Main"
    ) -> None:
        await self.async_command(
            utils.enable_audio_video_cmd(
                "Video", enable, channel, stream=stream
            )
        )
        await self.async_set_smart_ir(enable, channel)

    @property
    def video_out_options(self) -> str:
        return self._get_config("VideoOut")

    @property
    async def async_video_out_options(self) -> str:
        return await self._async_get_config("VideoOut")
