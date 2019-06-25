# -*- coding: utf-8 -*-
"""GPSCrest helpers."""
import logging

from gpscrest.objects import (
    GPSCrestCredentials, GPSCrestRaw, GPSCrestUserProfile, GPSDeviceLastPosition,
    GPSCrestDeviceTripDates)

_LOGGER = logging.getLogger(__name__)


def formatter_credentials(username, password):
        """Create GPSCrestCredentials NamedTuple."""
        return GPSCrestCredentials(username=username, password=password)

def formatter_crestraw(data):
    """Create GPSCrestRaw NamedTuple."""
    raw = GPSCrestRaw(
        name=data.get('name'),
        customer_id=data.get('customer_id'),
        token=data.get('token'),
        topic_id=data.get('topic_id'),
        gps_email=data.get('gps_email'),
        gps_phone=data.get('gps_phone'),
        hits=data.get('hits'),
        rate=data.get('rate')
    )
    return raw

def formatter_crest_user_profile(data):
    """Create GPSCrestUserProfile NamedTuple."""
    raw = GPSCrestUserProfile(
        id=data.get('id'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        email=data.get('email'),
        address=data.get('address'),
        city=data.get('city'),
        state=data.get('state'),
        zipcode=data.get('zipcode'),
        country=data.get('country'),
        company_name=data.get('company_name'),
        phone_numer=data.get('phone_numer'),
        customer_unique_id=data.get('customer_unique_id'),
        time_zone=data.get('time_zone'),
        language=data.get('language'),
        uom=data.get('uom'),
    )
    return raw


def formatter_device_last_position(data):
    """Create GPSDeviceLastPosition NamedTuple."""
    raw = GPSDeviceLastPosition(
        date=data.get('date'),
        time=data.get('time'),
        longitude=data.get('longitude'),
        latitude=data.get('latitude'),
        speed=data.get('speed'),
        speed_new=data.get('speed_new'),
        odometer_mileage=data.get('odometer_mileage'),
        battery_percentage=data.get('battery_percentage'),
        lastupdatestime=data.get('lastupdatestime'),
        lastlocation=data.get('lastlocation'),
        lastupdatestimeinmins=data.get('lastupdatestimeinmins'),
    )
    return raw


def formatter_device_trips_date(data):
    """Create GPSCrestDeviceTripDates NamedTuple."""
    raw = GPSCrestDeviceTripDates(
        dates=data
    )
    return raw


def assert_http_response(resp_json):
    """Assert if aiohttp response return code 200."""
    try:
        # API return string or intenger upon different name spaces 
        # this ensures we capture both scenarios
        assert resp_json['status'] == '200' or resp_json['status'] == 200
        return resp_json
    except:
        err = f"Error: {resp_json['DeveloperMessage']}: {resp_json['UsersMessage']}"
        _LOGGER.exception(err)
        raise Exception(err)


def formatter_trip_date(date_str):
    """Format date string from YYYYMMDD to MM/DD/YYYY."""
    year = date_str[:4]
    month = date_str[4:6]
    day = date_str[6:8]
    return f'{month}/{day}/{year}'
