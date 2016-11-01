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


class Audio:

    @property
    def audio_input_channels_numbers(self):
        ret = self.command(
            'devAudioInput.cgi?action=getCollect'
        )
        return ret.content.decode('utf-8')

    @property
    def audio_output_channels_numbers(self):
        ret = self.command(
            'devAudioOutput.cgi?action=getCollect'
        )
        return ret.content.decode('utf-8')
