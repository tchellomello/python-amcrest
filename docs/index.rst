.. Python Amcrest documentation master file, created by
   sphinx-quickstart on Fri Jun  2 01:30:31 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Python Amcrest's documentation!
==========================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

A Python 2.7/3.x module for `Amcrest Cameras <https://www.amcrest.com/>`_ using the SDK HTTP API.

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
    camera.ptz_control_command(action="start", code="Down", arg1=0, arg2=0, arg3=0)))

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

+-------------------------+---------------+----------+-----------------+
| Model                   |     Tested    | Status   | Results/Issues  |
+=========================+===============+==========+=================+
| IPM-721S                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP2M-841B/841W/842W     | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-956B               | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IP3M-956E               | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+
| IPM-HX1B                | Yes           |  working |                 |
+-------------------------+---------------+----------+-----------------+

If you have different model, feel fee to contribute and report your results.


----
Help
----
If you need any help, please join our community on the Gitter channels available at `Gitter <https://gitter.im/python-amcrest>`_.



Developing
==========

.. autoclass:: amcrest.AmcrestCamera
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.audio.Audio
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.event.Event
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.log.Log
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.motion_detection.MotionDetection
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.nas.Nas
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.network.Network
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.ptz.Ptz
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.record.Record
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.snapshot.Snapshot
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.special.Special
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.storage.Storage
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.system.System
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.user_management.UserManagement
    :members:
    :undoc-members:
    :show-inheritance:

.. autoclass:: amcrest.video.Video
    :members:
    :undoc-members:
    :show-inheritance:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
