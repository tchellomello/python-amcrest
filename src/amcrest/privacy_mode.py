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
        ret = self.command(
            f"configManager.cgi?action=setConfig&LeLensMask[0].Enable={mode}"
        )
        return ret.content.decode()

    def privacy_config(self) -> str:
        ret = self.command(
            "configManager.cgi?action=getConfig&name=LeLensMask"
        )
        return ret.content.decode()
