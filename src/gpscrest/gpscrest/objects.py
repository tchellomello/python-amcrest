from typing import NamedTuple


class GPSCrestCredentials(NamedTuple):
    username: str
    password: str


class GPSCrestRaw(NamedTuple):
    name: str
    customer_id: str
    token: str
    topic_id: str
    gps_email: str
    gps_phone: str
    hits: str
    rate: str


class GPSCrestUserProfile(NamedTuple):
    id: str
    first_name: str
    last_name: str
    email: str
    address: str
    city: str
    state: str
    zipcode: str
    country: str
    company_name: str
    phone_numer: str
    customer_unique_id: str
    time_zone: str
    language: str
    uom: str


class GPSDeviceLastPosition(NamedTuple):
    date: str
    time: str
    longitude: str
    latitude: str
    speed: str
    speed_new: str
    odometer_mileage: str
    battery_percentage: str
    lastupdatestime: str
    lastlocation: str
    lastupdatestimeinmins: str

class GPSCrestDeviceTripDates(NamedTuple):
    dates: list

    @property
    def total_days(self):
        """Total number of history days."""
        return len(self.dates)