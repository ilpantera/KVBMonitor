# KVB Monitor
The aim of this project is to display departures to a LED RGB matrix.

Credits for rgbmatrix library: https://github.com/hzeller/rpi-rgb-led-matrix

## Installation/ Activation
1. `apt-get install libjpeg9-dev`
2. `source bin/activate`
3. To install all of the requirements enter: `pip install -r requirements.txt`.
4. To run the script, enter: `sudo bin/python kvbmonitor.py`

Note: root privileges required due to LED matrix.

## Autostart
In order to activate the service and run it on every restart, execute (in KVBMonitor folder):
1. `chomod 755 launcher.sh` to make the service executable.
2. `cd` to navigate back to your home directory.
3. `mkdir logs` Create a logs directory.
4. `sudo crontab -e` Bring up crontab window.
5. Enter the following line `@reboot sh /home/pi/bbt/launcher.sh >/home/pi/logs/cronlog 2>&1` -> Will execute launcher.sh on startup.
6. `sudo reboot` and see if it works.
6a) if it does not work: `cd logs`followed by `cat cronlog`
