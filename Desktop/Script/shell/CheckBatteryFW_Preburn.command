#!/bin/sh

Battery_FW=`system_profiler SPPowerDataType | grep "Firmware Version" | head -1 | sed 's/.*: //'`

case $Battery_FW in 
*702* )
echo " [ Old Battery Firmware !!! ] "
echo "\033[32m [ 旧电池分位 ][请下载［5-10.15.0B1］］Bundle \033[30m"
;;

*901* )
echo " [ New Battery Firmware !!! ] "
echo "\033[31m [ 新电池分位 ][请下载［5-11.5.0A1］］Bundle \033[30m"
;;

* )
echo " [ Abnormal Battery Firmware , and pls contact TE !!! ] "
echo "\033[31m [ 不正常的电池分位，请联系TE，谢谢 ！！！] \033[30m"
;;
esac