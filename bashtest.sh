#!/bin/bash

x=0

while [ $x -le 10 ]; do

	echo $x

	if [ $x -eq 5 ]; then
		echo "X is five!  Woohoo!"

	fi

	x=$(( $x + 1 ))

done
