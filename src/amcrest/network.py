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
import socket
import threading
from contextlib import closing
from typing import List, Optional

from .http import Http


class Network(Http):

    amcrest_ips: List[str] = []
    __RTSP_PORT = 554
    __PWGPSI_PORT = 3800

    def __raw_scan(self, ipaddr: str, timeout: Optional[float] = None) -> None:
        if timeout:
            socket.setdefaulttimeout(timeout)
        else:
            # If devices not found, try increasing timeout
            socket.setdefaulttimeout(0.2)

        with closing(socket.socket()) as sock:
            try:
                sock.connect((ipaddr, self.__RTSP_PORT))
                sock.connect((ipaddr, self.__PWGPSI_PORT))
                self.amcrest_ips.append(ipaddr)

            # pylint: disable=bare-except
            except:
                pass

    def scan_devices(
        self, subnet: str, timeout: Optional[float] = None
    ) -> List[str]:
        """
        Scan cameras in a range of ips

        Params:
        subnet - subnet, i.e: 192.168.1.0/24
                 if mask not used, assuming mask 24

        timeout - timeout in sec

        Returns:
        """

        # Maximum range from mask
        # Format is mask: max_range
        max_range = {
            16: 256,
            24: 256,
            25: 128,
            27: 32,
            28: 16,
            29: 8,
            30: 4,
            31: 2,
        }

        # If user didn't provide mask, use /24
        if "/" not in subnet:
            mask = int(24)
            network = subnet
        else:
            network, mask_str = subnet.split("/")
            mask = int(mask_str)

        if mask not in max_range:
            raise RuntimeError("Cannot determine the subnet mask!")

        # Default logic is remove everything from last "." to the end
        # This logic change in case mask is 16
        network = network.rpartition(".")[0]

        if mask == 16:
            # For mask 16, we must cut the last two
            # entries with .

            # pylint: disable=unused-variable
            for i in range(0, 1):
                network = network.rpartition(".")[0]

        # Trigger the scan
        # For clear coding, let's keep the logic in if/else (mask16)
        # instead of only one if
        if mask == 16:
            for seq1 in range(max_range[mask]):
                for seq2 in range(max_range[mask]):
                    ipaddr = f"{network}.{seq1}.{seq2}"
                    thd = threading.Thread(
                        target=self.__raw_scan, args=(ipaddr, timeout)
                    )
                    thd.start()
        else:
            for seq1 in range(max_range[mask]):
                ipaddr = f"{network}.{seq1}"
                thd = threading.Thread(
                    target=self.__raw_scan, args=(ipaddr, timeout)
                )
                thd.start()

        return self.amcrest_ips

    @property
    def wlan_config(self) -> str:
        return self._get_config("WLan")

    @property
    async def async_wlan_config(self) -> str:
        return await self._async_get_config("WLan")

    @property
    def telnet_config(self) -> str:
        return self._get_config("Telnet")

    @telnet_config.setter
    def telnet_config(self, status: str) -> str:
        """
        status:
            false - Telnet is disabled
            true  - Telnet is enabled
        """
        ret = self.command(
            f"configManager.cgi?action=setConfig&Telnet.Enable={status}"
        )
        return ret.content.decode()

    @property
    async def async_telnet_config(self) -> str:
        return await self._async_get_config("Telnet")

    async def async_set_telnet_config(self, status: str) -> str:
        ret = await self.async_command(
            f"configManager.cgi?action=setConfig&Telnet.Enable={status}"
        )
        return ret.content.decode()

    @property
    def network_config(self) -> str:
        return self._get_config("Network")

    @property
    async def async_network_config(self) -> str:
        return await self._async_get_config("Network")

    @property
    def network_interfaces(self) -> str:
        ret = self.command("netApp.cgi?action=getInterfaces")
        return ret.content.decode()

    @property
    async def async_network_interfaces(self) -> str:
        ret = await self.async_command("netApp.cgi?action=getInterfaces")
        return ret.content.decode()

    @property
    def upnp_status(self) -> str:
        ret = self.command("netApp.cgi?action=getUPnPStatus")
        return ret.content.decode()

    @property
    async def async_upnp_status(self) -> str:
        ret = await self.async_command("netApp.cgi?action=getUPnPStatus")
        return ret.content.decode()

    @property
    def upnp_config(self) -> str:
        return self._get_config("UPnP")

    @upnp_config.setter
    def upnp_config(self, upnp_opt: str) -> str:
        """
        01/21/2017

        Note 1:
        -------
        The current SDK from Amcrest is case sensitive, do not
        mix UPPERCASE options with lowercase. Otherwise it will
        ignore your call.

        Example:

        Correct:
                "UPnP.Enable=true&UPnP.MapTable[0].Protocol=UDP"

        Incorrect:
            "UPnP.Enable=true&UPnP.Maptable[0].Protocol=UDP"
                                      ^ here should be T in UPPERCASE

        Note 2:
        -------
        In firmware Amcrest_IPC-AWXX_Eng_N_V2.420.AC00.15.R.20160908.bin
        InnerPort was not able to be changed as API SDK 2.10 suggests.

        upnp_opt is the UPnP options listed as example below:
        +-------------------------------------------------------------------+
        | ParamName                      | Value  | Description             |
        +--------------------------------+----------------------------------+
        |UPnP.Enable                     | bool   | Enable/Disable UPnP     |
        |UPnP.MapTable[index].Enable     | bool   | Enable/Disable UPnP map |
        |UPnP.MapTable[index].InnerPort  | int    | Range [1-65535]         |
        |UPnP.MapTable[index].OuterPort  | int    | Range [1-65535]         |
        |UPnP.MapTable[index].Protocol   | string | Range {TCP, UDP}        |
        |UPnP.MapTable[index].ServiceName| string | User UPnP Service name  |
        +-------------------------------------------------------------------+

        upnp_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """
        ret = self.command(f"configManager.cgi?action=setConfig&{upnp_opt}")
        return ret.content.decode()

    @property
    async def async_upnp_config(self) -> str:
        return await self._async_get_config("UPnP")

    async def async_set_upnp_config(self, upnp_opt: str) -> str:
        ret = await self.async_command(
            f"configManager.cgi?action=setConfig&{upnp_opt}"
        )
        return ret.content.decode()

    @property
    def ntp_config(self) -> str:
        return self._get_config("NTP")

    @ntp_config.setter
    def ntp_config(self, ntp_opt: str) -> str:
        """
        ntp_opt is the NTP options listed as example below:

        NTP.Address=clock.isc.org
        NTP.Enable=false
        NTP.Port=38
        NTP.TimeZone=9
        NTP.UpdatePeriod=31

        ntp_opt format:
        <paramName>=<paramValue>[&<paramName>=<paramValue>...]
        """
        ret = self.command(f"configManager.cgi?action=setConfig&{ntp_opt}")
        return ret.content.decode()

    @property
    async def async_ntp_config(self) -> str:
        return await self._async_get_config("NTP")

    async def async_set_ntp_config(self, ntp_opt: str) -> str:
        ret = await self.async_command(
            f"configManager.cgi?action=setConfig&{ntp_opt}"
        )
        return ret.content.decode()

    @property
    def rtsp_config(self) -> str:
        """Get RTSP configuration."""
        return self._get_config("RTSP")

    @property
    async def async_rtsp_config(self) -> str:
        """Get RTSP configuration."""
        return await self._async_get_config("RTSP")
