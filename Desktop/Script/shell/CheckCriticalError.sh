#!/bin/sh

return=`/usr/local/bin/hidreport -p 0x278 -i 0 get 0xe0 | grep -c '0000:	E0 20 00 00 00'`

if [ $return -eq 1 ];then
echo "Critical Error 0x20000000 found"
exit 1

else
exit 0
fi
