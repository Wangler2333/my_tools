#!/bin/sh

# For some reason, B0Am key may be changed to some non-default value.
# And this leads to that Battery can not charge
# Currently we believe it's process introduced.
# Check this key and report failure and meanwhile set this key's value to 10.
# 	Check it at startup, pre-burn and run-in set up.

value_B0Am=`/usr/local/bin/ypc2 -k B0Am`

if [ $value_B0Am -ne 10 ]; then
	echo "Unexpected B0Am vale: 0x${value_B0Am}"
	# Correct it
	echo "Correct it's value by running command: /usr/local/bin/ypc2 -wdk B0Am 0"
	/usr/local/bin/ypc2 -wdk B0Am 0
	exit 1
else
	echo "B0Am vale is expected: 0x${value_B0Am}"
	exit 0
fi