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

from .http import Http


# This API is based on an undocumented API of Amcrest Cameras.
# This API may change without notice
class PrivacyMode(Http):
    def set_privacy(self, mode: bool) -> str:
        """
        Params:
            mode         - True to enable privacy mode, false to disable

        Turns on privacy mode on or off in the camera
        """
        strM = str(mode).lower()
        ret = self.command(
            f"configManager.cgi?action=setConfig&LeLensMask[0].Enable={strM}"
        )
        return ret.content.decode()

    async def async_set_privacy(self, mode: bool) -> str:
        strM = str(mode).lower()
        ret = await self.async_command(
            f"configManager.cgi?action=setConfig&LeLensMask[0].Enable={strM}"
        )
        return ret.content.decode()

    def privacy_config(self) -> str:
        return self._get_config("LeLensMask")

    async def async_privacy_config(self) -> str:
        return await self._async_get_config("LeLensMask")
