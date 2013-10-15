#!/bin/bash

ipaddress="$(hostname -I)"

echo "Server started! Go to http://$ipaddress in your browser..."

sudo ./webcommander.py
