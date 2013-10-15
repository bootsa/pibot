#!/bin/bash

sudo amixer cset numid=3 1

sudo apt-get -y install alsa-utils espeak

echo -e "\n"

espeak "All is now ready!"

echo -e "\n\nTo run the server run the command './webcommander.py'\n\n" 
