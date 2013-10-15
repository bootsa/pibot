#!/bin/bash

sudo amixer cset numid=3 1

sudo apt-get -y install alsa-utils espeak python-virtualenv

virtualenv flask

echo -e "\n"

espeak "All is now ready!"

echo -e "\n\nTo start the server run the command './start.sh'\n\n" 
