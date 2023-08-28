#!/bin/bash

if [[ $UID != 0 ]]; then
    echo "Please run this script with sudo:"
    echo "sudo $0 $*"
    exit 1
fi

sudo rm -rf /usr/local/wthr/
sudo rm /usr/local/bin/wthr
