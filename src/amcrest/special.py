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


class Special(object):

    def realtime_stream(self, channel=1, typeno=0, path_file=None):
        """
        If the stream is redirect to a file, use mplayer tool to
        visualize the video record

        camera.realtime_stream(path_file="/home/user/Desktop/myvideo)
        $ mplayer /home/user/Desktop/myvideo
        """
        ret = self.command(
            'realmonitor.cgi?action=getStream&channel={0}&subtype={1}'.format(
                channel, typeno)
        )

        if path_file:
            with open(path_file, 'wb') as out_file:
                shutil.copyfileobj(ret.raw, out_file)

        return ret.raw

    def rtsp_url(self, channelno=None, typeno=None):
        """
        Return RTSP streaming url

        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        if channelno is None:
            channelno = 1

        if typeno is None:
            typeno = 0

        cmd = 'cam/realmonitor?channel={0}&subtype={1}'.format(
            channelno, typeno)

        return 'rtsp://{0}:{1}@{2}/{3}'.format(
            self._user, self._password, self._host, cmd)

    # pylint: disable=pointless-string-statement
    """
    11/05/2016

    Looks like the mjpeg support was removed from the mainstream in one of
    the firmware updates, so subtype=0 is not working.

    I have tested with the below firmware and still not working
    in the mainstream:
        Amcrest_IPC-AWXX_Eng_N_V2.420.AC00.15.R.20160908.bin

    Based on above, the cmd we send to camera should use: subtype=1 until
    mainstream is back.

    Simple translation:
        subtype=0 for mainstream
        subtype=1 for substream

    Tested on device: IP2M-841B

    Users complaining here too:
    https://amcrest.com/forum/technical-discussion-f3/lost-mjpeg-encode-for-main-stream-after-firmware-u-t1516.html
    """

    def mjpeg_url(self, channelno=None, typeno=None):
        """
        Return MJPEG streaming url

        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        if channelno is None:
            channelno = 0

        if typeno is None:
            typeno = 1

        cmd = "mjpg/video.cgi?channel={0}&subtype={1}".format(
            channelno, typeno)
        return '{0}{1}'.format(self._base_url, cmd)

    def mjpg_stream(self, channelno=None, typeno=None, path_file=None):
        """
        Params:
            channelno: integer, the video channel index which starts from 1,
                       default 1 if not specified.

            typeno: the stream type, default 0 if not specified. It can be
                    the following value:

                    0-Main Stream
                    1-Extra Stream 1 (Sub Stream)
                    2-Extra Stream 2 (Sub Stream)
        """
        cmd = self.mjpeg_url(channelno=channelno, typeno=typeno)
        ret = self.command(cmd)

        if path_file:
            with open(path_file, 'wb') as out_file:
                shutil.copyfileobj(ret.raw, out_file)

        return ret.raw
