#!/bin/sh
#set -x
Old="702"
New="901"
Battery_FW=`system_profiler SPPowerDataType | grep "Firmware Version" | head -1 | sed 's/.*: //'`
Bundle_B=`ls /Phoenix/Tables | grep "PGQ" | awk -F '.tb*' '{print$1}' | awk -F '_' '{print$3}'`

echo ; echo "\033[32m Battery Firmware : $Battery_FW \033[30m"  

case $Bundle_B in 
*5-10.15.0B2* )

echo ; echo "\033[32m Old Battery Firmware Bundle \033[30m" ; echo 

if [ "$Battery_FW" != "$Old" ];then 
echo "\033[31m Bundle下载错误，请重新下载正确的Bundle，需要下载【【5-11.5.0B2】】！！！\033[30m" ; echo 
exit 1
fi

echo "\033[32m Bundle下载正确，请继续测试！！! \033[30m" ; echo 
;;

*5-11.5.0B2* )
echo ; echo "\033[32m New Battery Firmware Bundle \033[30m" ; echo 

if [ "$Battery_FW" != "$New" ];then 
echo "\033[31m Bundle下载错误，请重新下载正确的Bundle，需要下载【【5-10.15.0B2】】！！！\033[30m" ; echo 
exit 1
fi

echo "\033[32m Bundle下载正确，请继续测试！！! \033[30m" ; echo 
;;

*5-11.7.0A2* )
echo ; echo "\033[32m New Battery Firmware Bundle \033[30m" ; echo 

if [ "$Battery_FW" != "$New" ];then 
echo "\033[31m Bundle下载错误，请重新下载正确的Bundle，需要下载【【5-11.7.0A2】】！！！\033[30m" ; echo 
exit 1
fi

echo "\033[32m Bundle下载正确，请继续测试！！! \033[30m" ; echo 
;;

* )
echo ; echo "\033[31m 没有Table或者Bundle不正常，请联系TE检查... \033[30m" ; echo
;;
esac



