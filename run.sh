#!/bin/bash

if [ "$EUID" -ne 0 ]; then
	echo "Please run as root"
	exit
fi

while true; do

	python3 PyFanControl.py
	exitcode=$?

	if [ $exitcode -eq 130 ]; then
		exit
	else
		cat errormail.txt | msmtp mr@ghorm.net
		/bin/bash ./fans_on.sh
		sleep 60

	fi

done
