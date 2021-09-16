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

    @property
    async def async_current_time(self) -> datetime:
        ret = await self.async_command("global.cgi?action=getCurrentTime")
        date_str = pretty(ret.content.decode())
        return str_to_date(date_str)

    async def async_set_current_time(self, date_value: datetime) -> bool:
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
        ret = await self.async_command(
            f"global.cgi?action=setCurrentTime&time={date_str}"
        )

        return "ok" in ret.content.decode().lower()

    @property
    def general_config(self) -> str:
        return self._get_config("General")

    @property
    async def async_general_config(self) -> str:
        return await self._async_get_config("General")

    @property
    def version_http_api(self) -> str:
        ret = self.command("IntervideoManager.cgi?action=getVersion&Name=CGI")
        return ret.content.decode()

    @property
    async def async_version_http_api(self) -> str:
        ret = await self.async_command(
            "IntervideoManager.cgi?action=getVersion&Name=CGI"
        )
        return ret.content.decode()

    @property
    def software_information(self) -> Tuple[str, str]:
        sw_info = self._magic_box("getSoftwareVersion")
        return self._parse_sw_information(sw_info)

    @property
    async def async_software_information(self) -> Tuple[str, str]:
        sw_info = await self._async_magic_box("getSoftwareVersion")
        return self._parse_sw_information(sw_info)

    @staticmethod
    def _parse_sw_information(swinfo: str) -> Tuple[str, str]:
        if "," in swinfo:
            version, build_date = swinfo.split(",")
        else:
            version, build_date = swinfo.split()
        _, _, version = version.rpartition("=")
        _, _, build_date = build_date.rpartition(":")
        return version, build_date

    @property
    def hardware_version(self) -> str:
        return pretty(self._magic_box("getHardwareVersion"))

    @property
    async def async_hardware_version(self) -> str:
        return pretty(await self._async_magic_box("getHardwareVersion"))

    @property
    def device_type(self) -> str:
        return pretty(self._magic_box("getDeviceType"))

    @property
    async def async_device_type(self) -> str:
        return pretty(await self._async_magic_box("getDeviceType"))

    @property
    def serial_number(self) -> str:
        return pretty(self._magic_box("getSerialNo"))

    @property
    async def async_serial_number(self) -> str:
        return pretty(await self._async_magic_box("getSerialNo"))

    @property
    def machine_name(self) -> str:
        return pretty(self._magic_box("getMachineName"))

    @property
    async def async_machine_name(self) -> str:
        return pretty(await self._async_magic_box("getMachineName"))

    @property
    def system_information(self) -> str:
        """System information

        Including serial number, device type, processor, and serial.
        """
        return self._magic_box("getSystemInfo")

    @property
    async def async_system_information(self) -> str:
        return await self._async_magic_box("getSystemInfo")

    @property
    def vendor_information(self) -> str:
        return pretty(self._magic_box("getVendor"))

    @property
    async def async_vendor_information(self) -> str:
        return pretty(await self._async_magic_box("getVendor"))

    @property
    def onvif_information(self) -> str:
        ret = self.command(
            "IntervideoManager.cgi?action=getVersion&Name=Onvif"
        )
        return ret.content.decode().strip()

    @property
    async def async_onvif_information(self) -> str:
        ret = await self.async_command(
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

    async def async_config_backup(
        self, filename: Optional[str] = None
    ) -> Optional[str]:
        ret = await self.async_command("Config.backup?action=All")

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
        return pretty(self._magic_box("getDeviceClass"))

    @property
    async def async_device_class(self) -> str:
        return pretty(await self._async_magic_box("getDeviceClass"))

    def shutdown(self) -> str:
        """
        From the testings, shutdown acts like "reboot now"
        """
        return self._magic_box("shutdown")

    async def async_shutdown(self) -> str:
        return await self._async_magic_box("shutdown")

    def reboot(self, delay: Optional[int] = None) -> str:
        cmd = "reboot"
        if delay:
            cmd += f"&delay={delay}"
        return self._magic_box(cmd)

    async def async_reboot(self, delay: Optional[int] = None) -> str:
        cmd = "reboot"
        if delay:
            cmd += f"&delay={delay}"
        return await self._async_magic_box(cmd)

    def onvif_login_check(self, setCheck: bool = False) -> str:
        """
        Allows the other non-admin accounts to use ONVIF.
        Currently only the 'admin' account can use ONVIF.
        """
        cmd = "configManager.cgi?action=setConfig"
        cmd += "&UserGlobal.OnvifLoginCheck={0}".format(str(setCheck).lower())
        ret = self.command(cmd)

        return ret.content.decode()

    async def async_onvif_login_check(self, setCheck: bool = False) -> str:
        """
        Allows the other non-admin accounts to use ONVIF.
        Currently only the 'admin' account can use ONVIF.
        """
        cmd = "configManager.cgi?action=setConfig"
        cmd += "&UserGlobal.OnvifLoginCheck={0}".format(str(setCheck).lower())
        ret = await self.async_command(cmd)

        return ret.content.decode()
