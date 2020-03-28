#!/bin/bash

brightness=20
columns=64
rows=32

if [ ! $(id -u) -eq 0 ]; then
    echo "Muss als root ausgeführt werden"
    exit 1
fi

sudo bin/python kvb-test.py --led-cols=$columns --led-rows=$rows --led-brightness=$brightness --led-pwm-lsb-nanoseconds=50
