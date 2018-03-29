#!/bin/sh

sudo nvram ResetNVRam=0 

sudo nvram boot-args="0x0"

sleep 1

shutdown -h now