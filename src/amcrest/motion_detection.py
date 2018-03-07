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
from amcrest.utils import str2bool


class MotionDetection(object):
    def __get_config(self, config_name):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(config_name)
        )
        return ret.content.decode('utf-8')

    @property
    def motion_detection(self):
        return self.__get_config("MotionDetect")

    def is_motion_detector_on(self):
        ret = self.motion_detection
        status = [s for s in ret.split() if '.Enable=' in s][0]\
            .split('=')[-1]
        return str2bool(status)  # pylint: disable=no-value-for-parameter

    def is_record_on_motion_detection(self):
        ret = self.motion_detection
        status = [s for s in ret.split() if '.RecordEnable=' in s][0]\
            .split('=')[-1]
        return str2bool(status)  # pylint: disable=no-value-for-parameter

    @motion_detection.setter
    def motion_detection(self, opt):
        if opt.lower() == "true" or opt.lower() == "false":
            ret = self.command(
                'configManager.cgi?action='
                'setConfig&MotionDetect[0].Enable={0}'.format(opt.lower())
            )
            if "ok" in ret.content.decode('utf-8').lower():
                return True

        return False

    @motion_detection.setter
    def motion_recording(self, opt):
        if opt.lower() == "true" or opt.lower() == "false":
            ret = self.command(
                'configManager.cgi?action='
                'setConfig&MotionDetect[0].EventHandler.RecordEnable={0}'
                .format(opt.lower())
            )
            if "ok" in ret.content.decode('utf-8').lower():
                return True

        return False
