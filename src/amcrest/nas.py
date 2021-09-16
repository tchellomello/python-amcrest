"""Amcrest NAS."""
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


class Nas(Http):
    """Amcrest methods to handle NAS."""

    @property
    def nas_information(self) -> str:
        """Return NAS information."""
        return self._get_config("NAS")

    @property
    async def async_nas_information(self) -> str:
        """Return NAS information."""
        return await self._async_get_config("NAS")
