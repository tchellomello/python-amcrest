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
from . import utils


class Video(object):
    @property
    def video_max_extra_stream(self):
        ret = self.command(
            "magicBox.cgi?action=getProductDefinition&name=MaxExtraStream"
        )
        return ret.content.decode("utf-8")

    @property
    def video_color_config(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoColor"
        )
        return ret.content.decode("utf-8")

    @property
    def encode_capability(self):
        ret = self.command("encode.cgi?action=getCaps")
        return ret.content.decode("utf-8")

    def encode_config_capability(self, channel):
        ret = self.command(
            "encode.cgi?action=getConfigCaps&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    @property
    def encode_media(self):
        ret = self.command("configManager.cgi?action=getConfig&name=Encode")
        return ret.content.decode("utf-8")

    @property
    def encode_region_interested(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoEncodeROI"
        )
        return ret.content.decode("utf-8")

    @property
    def video_channel_title(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=ChannelTitle"
        )
        return ret.content.decode("utf-8")

    # pylint: disable=invalid-name
    @property
    def video_input_channels_device_supported(self):
        ret = self.command("devVideoInput.cgi?action=getCollect")
        return ret.content.decode("utf-8")

    # pylint: disable=invalid-name
    @property
    def video_output_channels_device_supported(self):
        ret = self.command("devVideoOutput.cgi?action=getCollect")
        return ret.content.decode("utf-8")

    # pylint: disable=invalid-name
    @property
    def video_max_remote_input_channels(self):
        ret = self.command(
            "magicBox.cgi?action=getProductDefinition&name="
            "MaxRemoteInputChannels"
        )
        return ret.content.decode("utf-8")

    @property
    def video_standard(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoStandard"
        )
        return ret.content.decode("utf-8")

    @video_standard.setter
    def video_standard(self, std):
        ret = self.command(
            "configManager.cgi?action=setConfig&VideoStandard={0}".format(std)
        )
        return ret.content.decode("utf-8")

    @property
    def video_widget_config(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoWidget"
        )
        return ret.content.decode("utf-8")

    def video_input_capability(self, channel):
        ret = self.command(
            "devVideoInput.cgi?action=getCaps&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    def video_coordinates_current_window(self, channel):
        ret = self.command(
            "devVideoInput.cgi?action="
            "getCurrentWindow&channel={0}".format(channel)
        )
        return ret.content.decode("utf-8")

    @property
    def video_in_options(self):
        ret = self.command(
            "configManager.cgi?action=getConfig&name=VideoInOptions"
        )
        return ret.content.decode("utf-8")

    def video_in_option(self, param, profile="Day"):
        """
        Return video input option.

        Params:
            param - parameter, such as 'DayNightColor'
            profile - 'Day', 'Night' or 'Normal'
        """
        if profile == "Day":
            field = param
        else:
            field = "{}Options.{}".format(profile, param)
        return [
            utils.pretty(opt)
            for opt in self.video_in_options.split()
            if "].{}=".format(field) in opt
        ]

    def set_video_in_option(self, param, value, profile="Day", channel=0):
        if profile == "Day":
            field = param
        else:
            field = "{}Options.{}".format(profile, param)
        ret = self.command(
            "configManager.cgi?action=setConfig"
            "&VideoInOptions[{}].{}={}".format(channel, field, value)
        )
        return ret.content.decode("utf-8")

    def get_day_night_color(self, channel):
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        values = [int(x) for x in self.video_in_option("DayNightColor")]
        return values[channel]

    def set_day_night_color(self, value, channel):
        return self.set_video_in_option(
            "DayNightColor", value, channel=channel
        )

    def is_smart_ir_on(self, channel):
        """Return if SmartIR is on."""
        return self.video_in_option("InfraRed")[channel] == "false"

    def set_smart_ir(self, value, channel):
        # It's not clear why from the HTTP API SDK doc, but setting InfraRed
        # to false sets the Night Vision Mode to SmartIR, whereas setting it
        # to true sets the Night Vision Mode to OFF. Night Vision Mode has a
        # third setting of Manual, but that must be selected some other way
        # via the HTTP API.
        value = "false" if value else "true"
        return self.set_video_in_option("InfraRed", value, channel=channel)

    def is_video_enabled(self, channel):
        """Return if any video stream enabled."""
        is_enabled = utils.extract_audio_video_enabled(
            "Video", self.encode_media
        )
        return is_enabled[channel]

    def set_video_enabled(self, enable, channel):
        self.command(utils.enable_audio_video_cmd("Video", enable, channel))
        self.set_smart_ir(enable, channel)

    @property
    def day_night_color(self):
        """
        Return Day & Night Color Mode for Day profile.

        Result is 0: always multicolor
                  1: autoswitch along with brightness
                  2: always monochrome
        """
        return self.get_day_night_color(channel=0)

    @day_night_color.setter
    def day_night_color(self, value):
        return self.set_video_in_option("DayNightColor", value, channel=0)

    @property
    def smart_ir(self):
        """Return if SmartIR is on."""
        return self.is_smart_ir_on(channel=0)

    @smart_ir.setter
    def smart_ir(self, value):
        return self.set_smart_ir(value, channel=0)

    @property
    def video_enabled(self):
        """Return if any video stream enabled."""
        return self.is_video_enabled(channel=0)

    @video_enabled.setter
    def video_enabled(self, enable):
        self.set_video_enabled(enable, channel=0)

    @property
    def video_out_options(self):
        ret = self.command("configManager.cgi?action=getConfig&name=VideoOut")
        return ret.content.decode("utf-8")
