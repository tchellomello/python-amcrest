# -*- coding: utf-8 -*-
"""Constants used by GPSCrest."""

LAZY = True

BASE_URL = "https://amcrestgpstracker.com/staging/manage_gps_staging/api"
LOGIN_URL = f'{BASE_URL}/user/login'
PROFILE_URL = f'{BASE_URL}/user/get_profile'
IMEI_INFO_URL = f'{BASE_URL}/mapping_data/cutomer_imei_number_list_web'
COUNTRIES_URL = f'{BASE_URL}/zone/get_country_list'
TRIPS_DATE_URL = f'{BASE_URL}/user/get_user_tripsdate'
USER_TRIPS_URL = f'{BASE_URL}/user/get_user_trips'
USER_TRIPS_24HR_URL = f'{BASE_URL}/user/get_user_trips_24hr'

HEADERS = {
    'User-Agent': 
        'Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Referer': "https://amcrestgpstracker.com/",
    'Host': 'amcrestgpstracker.com',
}