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


class System:
    @property
    def current_time(self):
        ret = self.command(
            'global.cgi?action=getCurrentTime'
        )
        return ret.content.decode('utf-8')

    @current_time.setter
    def current_time(self, date):
        """
        According with API:
            The time format is "Y-M-D H-m-S". It’s not be effected by Locales.
            TimeFormat in SetLocalesConfig

        Params:
            date = "Y-M-D H-m-S"
            Example: 2016-10-28 13:48:00

        Return: True
        """
        ret = self.command(
            'global.cgi?action=setCurrentTime&time={0}'.format(date)
        )

        if "ok" in ret.content.decode('utf-8').lower():
            return True

        return False

    def __get_config(self, config_name):
        ret = self.command(
            'configManager.cgi?action=getConfig&name={0}'.format(config_name)
        )
        return ret.content.decode('utf-8')

    @property
    def general_config(self):
        return self.__get_config('General')
