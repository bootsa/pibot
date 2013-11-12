#!/bin/bash

sudo amixer cset numid=3 1

sudo apt-get -y install alsa-utils espeak ipython python-setuptools python-virtualenv

sudo easy_install -U RPIO

virtualenv flask

echo -e "\n"

espeak "pibot is now ready!"
