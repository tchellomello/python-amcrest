"""Amcrest system module."""
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


class System(object):
    """Amcrest system class."""
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
            The time format is "Y-M-D H-m-S". It is not be effected by Locales.
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

    @property
    def version_http_api(self):
        ret = self.command(
            'IntervideoManager.cgi?action=getVersion&Name=CGI'
        )
        return ret.content.decode('utf-8')

    @property
    def software_information(self):
        ret = self.command(
            'magicBox.cgi?action=getSoftwareVersion'
        )
        swinfo = ret.content.decode('utf-8')
        if ',' in swinfo:
            version, build_date = swinfo.split(',')
        else:
            version, build_date = swinfo.split()
        return (version, build_date)

    @property
    def hardware_version(self):
        ret = self.command(
            'magicBox.cgi?action=getHardwareVersion'
        )
        return ret.content.decode('utf-8')

    @property
    def device_type(self):
        ret = self.command(
            'magicBox.cgi?action=getDeviceType'
        )
        return ret.content.decode('utf-8')

    @property
    def serial_number(self):
        ret = self.command(
            'magicBox.cgi?action=getSerialNo'
        )
        return ret.content.decode('utf-8').split('=')[-1]

    @property
    def machine_name(self):
        ret = self.command(
            'magicBox.cgi?action=getMachineName'
        )
        return ret.content.decode('utf-8')

    @property
    def system_information(self):
        ret = self.command(
            'magicBox.cgi?action=getSystemInfo'
        )
        return ret.content.decode('utf-8')

    @property
    def vendor_information(self):
        ret = self.command(
            'magicBox.cgi?action=getVendor'
        )
        return ret.content.decode('utf-8')

    @property
    def onvif_information(self):
        ret = self.command(
            'IntervideoManager.cgi?action=getVersion&Name=Onvif'
        )
        return ret.content.decode('utf-8')

    def config_backup(self, filename=None):
        ret = self.command(
            'Config.backup?action=All'
        )

        if not ret:
            return None

        if filename:
            with open(filename, "w+") as cfg:
                cfg.write(ret.content.decode('utf-8'))
            return None

        return ret.content.decode('utf-8')

    @property
    def device_class(self):
        """
        During the development, device IP2M-841B didn't
        responde for this call, adding it anyway.
        """
        ret = self.command(
            'magicBox.cgi?action=getDeviceClass'
        )
        return ret.content.decode('utf-8')

    def shutdown(self):
        """
        From the testings, shutdown acts like "reboot now"
        """
        ret = self.command(
            'magicBox.cgi?action=shutdown'
        )
        return ret.content.decode('utf-8')

    def reboot(self, delay=None):
        cmd = 'magicBox.cgi?action=reboot'

        if delay:
            cmd += "&delay={0}".format(delay)

        ret = self.command(cmd)
        return ret.content.decode('utf-8')
