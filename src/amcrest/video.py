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


class Video(object):

    @property
    def video_max_extra_stream(self):
        ret = self.command(
            'magicBox.cgi?action=getProductDefinition&name=MaxExtraStream'
        )
        return ret.content.decode('utf-8')

    @property
    def video_color_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoColor'
        )
        return ret.content.decode('utf-8')

    @property
    def encode_capability(self):
        ret = self.command(
            'encode.cgi?action=getCaps'
        )
        return ret.content.decode('utf-8')

    def encode_config_capability(self, channel):
        ret = self.command(
            'encode.cgi?action=getConfigCaps&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    @property
    def encode_media(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=Encode'
        )
        return ret.content.decode('utf-8')

    @property
    def encode_region_interested(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoEncodeROI'
        )
        return ret.content.decode('utf-8')

    @property
    def video_channel_title(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=ChannelTitle'
        )
        return ret.content.decode('utf-8')

    # pylint: disable=invalid-name
    @property
    def video_input_channels_device_supported(self):
        ret = self.command(
            'devVideoInput.cgi?action=getCollect'
        )
        return ret.content.decode('utf-8')

    # pylint: disable=invalid-name
    @property
    def video_output_channels_device_supported(self):
        ret = self.command(
            'devVideoOutput.cgi?action=getCollect'
        )
        return ret.content.decode('utf-8')

    # pylint: disable=invalid-name
    @property
    def video_max_remote_input_channels(self):
        ret = self.command(
            'magicBox.cgi?action=getProductDefinition&name='
            'MaxRemoteInputChannels'
        )
        return ret.content.decode('utf-8')

    @property
    def video_standard(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoStandard'
        )
        return ret.content.decode('utf-8')

    @video_standard.setter
    def video_standard(self, std):
        ret = self.command(
            'configManager.cgi?action=setConfig&VideoStandard={0}'.format(std)
        )
        return ret.content.decode('utf-8')

    @property
    def video_widget_config(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoWidget'
        )
        return ret.content.decode('utf-8')

    def video_input_capability(self, channel):
        ret = self.command(
            'devVideoInput.cgi?action=getCaps&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    def video_coordinates_current_window(self, channel):
        ret = self.command(
            'devVideoInput.cgi?action='
            'getCurrentWindow&channel={0}'.format(channel)
        )
        return ret.content.decode('utf-8')

    @property
    def video_in_options(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoInOptions'
        )
        return ret.content.decode('utf-8')

    @property
    def video_out_options(self):
        ret = self.command(
            'configManager.cgi?action=getConfig&name=VideoOut'
        )
        return ret.content.decode('utf-8')
