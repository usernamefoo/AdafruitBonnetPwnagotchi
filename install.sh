#!/bin/sh

pip3 install adafruit-circuitpython-ssd1306
cp -r ./hw /usr/local/lib/python3.7/dist-packages/pwnagotchi/ui/
patch --directory=/usr/local/lib/python3.7/dist-packages/pwnagotchi -p2 < adafruitoled.patch
