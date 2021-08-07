"""Amcrest system module."""
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

from datetime import datetime
from typing import Optional, Tuple

from .http import Http
from .utils import date_to_str, pretty, str_to_date


class System(Http):
    """Amcrest system class."""

    @property
    def current_time(self) -> datetime:
        ret = self.command("global.cgi?action=getCurrentTime")
        date_str = pretty(ret.content.decode())
        return str_to_date(date_str)

    @current_time.setter
    def current_time(self, date_value: datetime) -> bool:
        """
        According with API:
            The time format is "Y-M-D H-m-S". It is not be effected by Locales.
            TimeFormat in SetLocalesConfig

        Params:
            date = "Y-M-D H-m-S"
            Example: 2016-10-28 13:48:00

        Return: True
        """
        date_str = date_to_str(date_value)
        ret = self.command(f"global.cgi?action=setCurrentTime&time={date_str}")

        return "ok" in ret.content.decode().lower()

    def __get_config(self, config_name: str) -> str:
        ret = self.command(
            f"configManager.cgi?action=getConfig&name={config_name}"
        )
        return ret.content.decode()

    @property
    def general_config(self) -> str:
        return self.__get_config("General")

    @property
    def version_http_api(self) -> str:
        ret = self.command("IntervideoManager.cgi?action=getVersion&Name=CGI")
        return ret.content.decode()

    @property
    def software_information(self) -> Tuple[str, str]:
        ret = self.command("magicBox.cgi?action=getSoftwareVersion")
        swinfo = ret.content.decode().strip()
        if "," in swinfo:
            version, build_date = swinfo.split(",")
        else:
            version, build_date = swinfo.split()
        _, _, version = version.rpartition("=")
        _, _, build_date = build_date.rpartition(":")
        return version, build_date

    @property
    def hardware_version(self) -> str:
        ret = self.command("magicBox.cgi?action=getHardwareVersion")
        return ret.content.decode().strip()

    @property
    def device_type(self) -> str:
        ret = self.command("magicBox.cgi?action=getDeviceType")
        return pretty(ret.content.decode())

    @property
    def serial_number(self) -> str:
        ret = self.command("magicBox.cgi?action=getSerialNo")
        return pretty(ret.content.decode())

    @property
    def machine_name(self) -> str:
        ret = self.command("magicBox.cgi?action=getMachineName")
        return pretty(ret.content.decode())

    @property
    def system_information(self) -> str:
        """System information

        Including serial number, device type, processor, and serial.
        """
        ret = self.command("magicBox.cgi?action=getSystemInfo")
        return ret.content.decode()

    @property
    def vendor_information(self) -> str:
        ret = self.command("magicBox.cgi?action=getVendor")
        return ret.content.decode().strip()

    @property
    def onvif_information(self) -> str:
        ret = self.command(
            "IntervideoManager.cgi?action=getVersion&Name=Onvif"
        )
        return ret.content.decode().strip()

    def config_backup(self, filename: Optional[str] = None) -> Optional[str]:
        ret = self.command("Config.backup?action=All")

        if not ret:
            return None

        if filename:
            with open(filename, "w+") as cfg:
                cfg.write(ret.content.decode())
            return None

        return ret.content.decode()

    @property
    def device_class(self) -> str:
        """
        During the development, device IP2M-841B didn't
        responde for this call, adding it anyway.
        """
        ret = self.command("magicBox.cgi?action=getDeviceClass")
        return pretty(ret.content.decode())

    def shutdown(self) -> str:
        """
        From the testings, shutdown acts like "reboot now"
        """
        ret = self.command("magicBox.cgi?action=shutdown")
        return ret.content.decode()

    def reboot(self, delay: Optional[int] = None) -> str:
        cmd = "magicBox.cgi?action=reboot"

        if delay:
            cmd += f"&delay={delay}"

        ret = self.command(cmd)
        return ret.content.decode()

    def onvif_login_check(self, setCheck: bool = False) -> str:
        """
        Allows the other non-admin accounts to use ONVIF.
        Currently only the 'admin' account can use ONVIF.
        """
        cmd = 'configManager.cgi?action=setConfig'
        cmd += "&UserGlobal.OnvifLoginCheck={0}".format(str(setCheck).lower())
        ret = self.command(cmd)

        return ret.content.decode()
