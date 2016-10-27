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


class MotionDetection:
    def __get_config(self, config_name):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(config_name)
        )
        return ret.content.decode('utf-8')

    @property
    def motion_detection(self):
        return self.__get_config("MotionDetect")

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
