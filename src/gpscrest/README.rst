==============
Python GPS Amcrest
==============

An Async Python 3.x module for `Amcrest GPS Tracker <https://amcrestgpstracker.com>`_.

------------
Installation
------------

TODO

-----
Usage
-----

.. code-block:: python

    import asyncio
    from gpscrest.core import GPSCrest

    loop = asyncio.get_event_loop()
    gps = GPSCrest('username', 'password', lazy=False)
    loop.run_until_complete(gps.run())

    gps
    <GPSCrest: 12345redacted>

    gps.devices
    [<GPSCrestDevice: amcrest-4g>]

    gps.user_profile
    GPSCrestUserProfile(id='1234', first_name='John', last_name='Doe', email='jdoe@example.com', address='1234 North Main St.', city='New York', state='New York', zipcode='12345', country='250', company_name='', phone_numer=None, customer_unique_id='999999', time_zone=' (UTC-05:00) Eastern Time (US and Canada)', language='en', uom='2')

    gps.user_profile.email
    'jdoe@example.com'

    tracker = gps.devices[0]

    tracker.battery
    '100'

    tracker.imei_number
    '01518100099999999'

    tracker.latitude
    '35.1234567'

    tracker.longitude
    '-78.1245677'

    tracker.odometer_mileage
    '1851.69 Miles'

    tracker.speed
    '25 Mp/h'

    tracker.trips_date
    GPSCrestDeviceTripDates(dates=['20190517', '20190518', '20190519', '20190520', '20190521', '20190522', '20190523', '20190524', '20190525', '20190526', '20190527', '20190528', '20190529', '20190530', '20190531', '20190601', '20190602', '20190603', '20190605', '20190607', '20190608', '20190609', '20190610', '20190611', '20190612', '20190614', '20190615', '20190616', '20190617', '20190618', '20190619', '20190620', '20190621', '20190622', '20190623', '20190624'])


----
NOTE
----
This code is still under alpha development. 
