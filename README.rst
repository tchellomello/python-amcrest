==============
Python Amcrest
==============

.. image:: https://badge.fury.io/py/amcrest.svg
    :target: https://badge.fury.io/py/amcrest

.. image:: https://travis-ci.org/tchellomello/python-amcrest.svg?branch=master
    :target: https://travis-ci.org/tchellomello/python-amcrest

.. image:: https://coveralls.io/repos/github/tchellomello/python-amcrest/badge.svg
    :target: https://coveralls.io/github/tchellomello/python-amcrest

.. image:: https://img.shields.io/pypi/pyversions/amcrest.svg
    :target: https://pypi.python.org/pypi/amcrest

A Python 2.7/3.x module for `Amcrest Cameras <https://www.amcrest.com/>`_ using the SDK HTTP API. Amcrest and Dahua devices share similar firmwares. Dahua Cameras and NVRs also work with this module.

Documentation: `http://python-amcrest.readthedocs.io/ <http://python-amcrest.readthedocs.io/>`_

------------
Installation
------------

PyPI
----

.. code-block:: bash

    $ pip install amcrest --upgrade
    $ eval "$(register-python-argcomplete amcrest-cli)"

    # To enable amcrest-cli autocomplete in the system:
    $ echo 'eval "$(register-python-argcomplete amcrest-cli)"' >  /etc/profile.d/amcrest-cli-autocomplete.sh

RPM
---

.. code-block:: bash

    $ git clone git@github.com:tchellomello/python-amcrest.git
    $ ./autogen.sh
    $ make rpm
    $ dnf/yum install amcrest-cli-NVR.rpm pythonX-amcrest-NVR.rpm


-----
Usage
-----

.. code-block:: python

    from amcrest import AmcrestCamera
    camera = AmcrestCamera('192.168.0.1', 80, 'admin', 'password').camera

    #Check software information
    camera.software_information
    'version=2.420.AC00.15.R\r\nBuildDate=2016-09-08'

    #Capture snapshot
    camera.snapshot(0, "/home/user/Desktop/snapshot00.jpeg")
    <requests.packages.urllib3.response.HTTPResponse object at 0x7f84945083c8>

    #Capture audio
    camera.audio_stream_capture(httptype="singlepart", channel=1, path_file="/home/user/Desktop/audio.aac")
    CTRL-C to stop the continuous audio flow or use a timer

    #Move camera down
    camera.ptz_control_command(action="start", code="Down", arg1=0, arg2=0, arg3=0)

    #Record realtime stream into a file
    camera.realtime_stream(path_file="/home/user/Desktop/myvideo")
    CTRL-C to stop the continuous video flow or use a timer

Command Line
------------

.. code-block:: bash

    $ man amcrest-cli
    or
    $ amcrest-cli --help

    # Saving credentials to file.
    $ vim ~/.config/amcrest.conf
    [patio]
    hostname: 192.168.0.20
    username: admin
    password: 123456
    port: 80

    [living_room]
    hostname: 192.168.0.21
    username: admin
    password: secret
    port: 80

    $ amcrest-cli --camera living_room --version-http-api
    version=1.40

Text User Interface (TUI)
-------------------------
Configure amcrest.conf and trigger amcrest-tui, make sure the user
triggering amcrest-tui have access to framebuffer device or use sudo.

*NOTE:*
Execute it from console logins, like /dev/ttyX (Non X Window).
Pseudo-terminals like xterm, ssh, screen and others WONT WORK.

.. code-block:: bash

    $ vim ~/.config/amcrest.conf
    [patio]
    hostname: 192.168.0.20
    username: admin
    password: 123456
    port: 80

    [living_room]
    hostname: 192.168.0.21
    username: admin
    password: secret
    port: 80

    $ amcrest-tui


---------------------
Supportability Matrix
---------------------

Cameras
-------

+-------------------------+---------------+----------+-----------------+
| Model                   |     Tested    | Status   | Results/Issues  |
+=========================+===============+==========+=================+
| IPM-721                 | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IPM-HX1                 | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP2M-841                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP2M-842                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-941                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-943                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-956                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-956E               | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-HX2                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP4M-1026B              | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP4M-1051B              | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP5M-1176EB             | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP8M-2496EB             | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP8M-T2499EW-28M        | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+


Network Video Recorders (NVR)
-----------------------------

+-------------------------+---------------+----------+-----------------+
| Model                   |     Tested    | Status   | Results/Issues  |
+=========================+===============+==========+=================+
| XVR DAHUA 5104S         | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+


If you have different model, feel fee to contribute and report your results.


----
Help
----
If you need any help, please join our community on the Gitter channels available at `Gitter <https://gitter.im/python-amcrest>`_.
