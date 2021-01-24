#!/bin/bash

while true; do
	python3 PyFanControl.py

	if [ $? == 130 ]; then
		exit 0
	fi

done
