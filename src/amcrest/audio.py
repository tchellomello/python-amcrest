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
import shutil


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

    def audio_stream_capture(self, httptype=None,
                             channel=None, path_file=None):
        """
        Params:

            path_file - path to output file
            channel: - integer
            httptype - type string (singlepart or multipart)

                singlepart: HTTP content is a continuos flow of audio packets
                multipart: HTTP content type is multipart/x-mixed-replace, and
                           each audio packet ends with a boundary string

        """
        if httptype is None and channel is None:
            raise RuntimeError("Requires htttype and channel")

        ret = self.command(
            'audio.cgi?action=getAudio&httptype={0}&channel={1}'.format(
                httptype, channel))

        if path_file:
            with open(path_file, 'wb') as out_file:
                shutil.copyfileobj(ret.raw, out_file)

        return ret.raw
