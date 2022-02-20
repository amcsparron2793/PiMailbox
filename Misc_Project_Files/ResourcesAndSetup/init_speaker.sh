#!/bin/bash

# This script uses curl to download the i2samp.sh setup script.
# It then pipes it directly to bash without saving it.

url_i2s_setup=https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/i2samp.sh

curl -sS $url_i2s_setup | bash