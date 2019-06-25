import asyncio
import logging

from gpscrest.base import GPSCrestBase
from gpscrest.objects import GPSCrestDeviceTripDates
from gpscrest.constants import (
    TRIPS_DATE_URL, USER_TRIPS_24HR_URL, USER_TRIPS_URL)
from gpscrest.helpers import (
    formatter_device_trips_date, formatter_trip_date)


_LOGGER = logging.getLogger(__name__)

class GPSCrestDevice(GPSCrestBase):

    def __init__(self, response, parent):
        super().__init__()
        self._name = response.get('name')
        self._imei_number = response.get('imei_number')
        self._parent = parent
        self.trips_date: GPSCrestDeviceTripDates = None

    async def _preload(self):
        """Methods to preload object in background."""
        await asyncio.gather(
            self.get_trips_date(),
        )

        await asyncio.gather(
            self.get_user_trips(),
        )


    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}: {self.name}>'

    @property
    def name(self) -> str:
        return self._name

    @property
    def imei_number(self) -> str:
        return self._imei_number

    @property
    def last_location(self) -> str:
        return self._info.lastlocation

    @property
    def last_update_time(self) -> str:
        return self._info.lastupdatestime

    @property
    def last_update_in_mins(self) -> str:
        return self._info.lastupdatestimeinmins

    @property
    def battery(self) -> str:
        return self._info.battery_percentage

    @property
    def longitude(self) -> str:
        return self._info.longitude

    @property
    def latitude(self) -> str:
        return self._info.latitude

    @property
    def speed(self) -> str:
        return self._info.speed

    @property
    def odometer_mileage(self) -> str:
        return self._info.odometer_mileage

    async def get_trips_date(self) -> str:
        """Gather trips date for the given imei number."""
        data = {'imei': self.imei_number}
        self.trips_date = formatter_device_trips_date(
            await self._parent.Fetcher.post(url=TRIPS_DATE_URL,
                                            data=data,
                                            headers=self._headers))

    async def get_user_trips(self) -> str:
        """
        Gather trips date for the given imei number.

        This method will schedule all trips in
        the event loop and run it async.
        """

        tasks = []
        for date in self.trips_date.dates:
            data = {
                'imei': self.imei_number,
                'date': formatter_trip_date(date)
            }
            print(f'ok -> {data}')
            task = asyncio.ensure_future(
                self._parent.Fetcher.post(
                    url=USER_TRIPS_URL,
                    data=data,
                    headers=self._headers
                )
            )
            tasks.append(task)

        response = await asyncio.gather(*tasks)
        print(response)




class GPSCrestDeviceTrips:

    def __init__(self):
        pass
