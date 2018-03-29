#!/bin/sh

UUID=`diskutil info DATA | grep "Volume UUID" | sed 's/.*: //'`
echo $UUID