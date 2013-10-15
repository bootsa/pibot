#!/bin/bash

$ipaddress = hostname -i

echo "Server started! Go to $ipaddress in your browser..."

sudo ./webcommander.py
