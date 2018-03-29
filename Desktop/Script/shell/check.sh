#!/bin/sh

#diskutil partitionDisk /dev/$1 1 GPTFormat HFS+ Diagnostics 1G


diskutil info $1