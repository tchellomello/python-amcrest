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
import logging
import shutil
from typing import Optional

from urllib3.exceptions import HTTPError  # type: ignore[import]

from . import utils
from .exceptions import CommError
from .http import Http

_LOGGER = logging.getLogger(__name__)


class Audio(Http):
    @property
    def audio_input_channels_numbers(self) -> str:
        ret = self.command("devAudioInput.cgi?action=getCollect")
        return ret.content.decode()

    @property
    def audio_output_channels_numbers(self) -> str:
        ret = self.command("devAudioOutput.cgi?action=getCollect")
        return ret.content.decode()

    def play_wav(
        self, httptype=None, channel=None, path_file=None, encoding="G.711A"
    ) -> None:
        if httptype is None:
            httptype = "singlepart"

        if channel is None:
            channel = "1"

        if path_file is None:
            raise RuntimeError("filename is required")

        self.audio_send_stream(httptype, channel, path_file, encoding)

    def audio_send_stream(
        self, httptype=None, channel=None, path_file=None, encode=None
    ) -> None:
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

        header = {"content-type": "Audio/" + encode, "content-length": "9999999"}

        with open(path_file, "rb") as f:
            file_audio = {"file": f}
            self.command_audio(
                f"audio.cgi?action=postAudio&httptype={httptype}&channel={channel}",
                file_content=file_audio,
                http_header=header,
            )

    def audio_stream_capture(
        self,
        httptype: Optional[str] = None,
        channel: Optional[int] = None,
        path_file: Optional[str] = None,
    ) -> bytes:
        """
        Params:
            httptype - type string (singlepart or multipart)
                singlepart: HTTP content is a continuos flow of audio packets
                multipart: HTTP content type is multipart/x-mixed-replace, and
                           each audio packet ends with a boundary string
            channel - integer
            path_file - path to output file
        """
        if httptype is None and channel is None:
            raise RuntimeError("Requires htttype and channel")

        ret = self.command(
            f"audio.cgi?action=getAudio&httptype={httptype}&channel={channel}",
            stream=True,
        )

        if path_file:
            try:
                with open(path_file, "wb") as out_file:
                    shutil.copyfileobj(ret.raw, out_file)
            except HTTPError as error:
                _LOGGER.debug(
                    "%s Audio stream capture to file failed due to error: %s",
                    self,
                    repr(error),
                )
                raise CommError(error)

        return ret.raw

    def is_audio_enabled(self, *, channel: int = 0) -> bool:
        """Return if any audio stream enabled."""
        is_enabled = utils.extract_audio_video_enabled(
            "Audio", self.encode_media_config
        )
        return is_enabled[channel]

    def set_audio_enabled(self, enable: bool, *, channel: int = 0) -> None:
        """Enable/disable all audio streams."""
        self.command(utils.enable_audio_video_cmd("Audio", enable, channel))

    @property
    def encode_media_config(self) -> str:
        ret = self.command("configManager.cgi?action=getConfig&name=Encode")
        return ret.content.decode()
