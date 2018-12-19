# service.PowerControl

Simple Plugin for Kodi on Raspberry Pi / LibreELEC to turn the unit off through GPIO. Additionally it signals "LOW" on a second pin to show the unit is alive/powered on. Both pins are configurable, service needs to be restarted for changes to take effect.

Requires virtual.rpi-tools to be installed! This is not added to the addon requirements yet.

This is intended for use with something like an Arduino to communicate with the Rpi, so it knows whenit's on, and can it turn off again. See/github.com/Xoliul/PowerMan repo for example.
