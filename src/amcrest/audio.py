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

from . import utils


class Audio(object):

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

    def play_wav(self, httptype=None, channel=None,
                 path_file=None):

        if httptype is None:
            httptype = 'singlepart'

        if channel is None:
            channel = '1'

        if path_file is None:
            raise RuntimeError('filename is required')

        self.audio_send_stream(httptype, channel, path_file, 'G.711A')

    def audio_send_stream(self, httptype=None,
                          channel=None, path_file=None, encode=None):
        """
        Params:

            path_file - path to audio file
            channel: - integer
            httptype - type string (singlepart or multipart)

                singlepart: HTTP content is a continuos flow of audio packets
                multipart: HTTP content type is multipart/x-mixed-replace, and
                           each audio packet ends with a boundary string

            Supported audio encode type according with documentation:
                PCM
                ADPCM
                G.711A
                G.711.Mu
                G.726
                G.729
                MPEG2
                AMR
                AAC

        """
        if httptype is None or channel is None:
            raise RuntimeError("Requires htttype and channel")

        file_audio = {
            'file': open(path_file, 'rb'),
        }

        header = {
            'content-type': 'Audio/' + encode,
            'content-length': '9999999'
        }

        self.command_audio(
            'audio.cgi?action=postAudio&httptype={0}&channel={1}'.format(
                httptype, channel),
            file_content=file_audio,
            http_header=header
        )

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

    @property
    def audio_enabled(self):
        """Return if any audio stream enabled."""
        return utils.extract_audio_video_enabled('Audio', self.encode_media)

    @audio_enabled.setter
    def audio_enabled(self, enable):
        """Enable/disable all audio streams."""
        self.command(utils.enable_audio_video_cmd('Audio', enable))
