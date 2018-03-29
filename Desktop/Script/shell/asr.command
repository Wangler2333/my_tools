#!/bin/sh
	
diskutil list

sudo -S diskutil partitionDisk /dev/disk2 1 GPTFormat HFS+ Diagnostics 1g

sudo asr -partition /dev/disk2 -testsize 100g -retestsize 5g -recoverysize 18g

sudo diskutil resizeVolume disk2s3 90g %5361644d-6163-11AA-AA11-00306543ECAC% KernelCore 4g

sudo -S sudo asr -s /Users/beck/Downloads/J137_EVT-25_0_LoboEldorado17A12820q_PyramidEldorado15P11660p_0_3842.dmg  -t /dev/disk2s3 -erase -noverify -noprompt




