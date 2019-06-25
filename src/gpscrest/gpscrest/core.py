"""Amcrest GPS Python wrapper."""
import asyncio
import logging

from gpscrest.constants import (
    LOGIN_URL, PROFILE_URL, IMEI_INFO_URL, LAZY)
from gpscrest.helpers import (
    formatter_crestraw, formatter_credentials, formatter_device_last_position,
    formatter_crest_user_profile, assert_http_response)

from gpscrest.fetcher import GPSCrestFetcher
from gpscrest.device import GPSCrestDevice
from gpscrest.base import GPSCrestBase


_LOGGER = logging.getLogger(__name__)

PROXY = 'http://localhost:9090'

class GPSCrest(GPSCrestBase):

    def __init__(self, username: str, password: str, proxy=None, lazy: bool=LAZY):
        """Base class for GPSCrest."""
        super().__init__()
        self.__credentials: str = formatter_credentials(username, password)
        self._lazy = lazy

        self.Fetcher = GPSCrestFetcher(proxy=proxy)

        self.devices: list = None
        self.user_profile: dict  = None

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.customer_id}>'

    @property
    def name(self) -> str:
        return self._info.name

    @property
    def gps_email(self) -> str:
        return self._info.gps_email

    @property
    def gps_phone(self) -> str:
        return self._info.gps_phone

    async def run(self):
        raw = await self.fetch_token()
        self._info = formatter_crestraw(raw)
        self.devices = [GPSCrestDevice(device, self) for device in raw.get('imeilist')]

        ## another way to schedule it
        tasks = []
        tasks.append(asyncio.ensure_future(self.get_user_profile()))
        tasks.append(asyncio.ensure_future(self.get_imei_info()))
        tasks.append(asyncio.ensure_future(self.get_country_list()))
        await asyncio.gather(*tasks)

        ## whenener self.lazy is True, then preload
        ## date on each device such as trip_dates and date per day
        if not self.lazy:
            [await device._preload() for device in self.devices]

    async def fetch_token(self):
        """Fetch token and initialize object."""
        data = {
            'email': self.__credentials.username,
            'password': self.__credentials.password
        }
        return await self.Fetcher.post(url=LOGIN_URL, data=data)

    async def get_user_profile(self):
        """Populate GPSCrestUserProfile attribute."""
        self.user_profile = formatter_crest_user_profile(
            await self.Fetcher.post(url=PROFILE_URL, headers=self._headers))

    async def get_imei_info(self):
        """Populate latest data of a GPS device."""
        response = await self.Fetcher.post(url=IMEI_INFO_URL, headers=self._headers)
        for parent_device in self.devices:
            for device in response:
                if parent_device.imei_number == device.get('imei'):
                    parent_device._info = formatter_device_last_position(device)
