#!/bin/sh

M8=`system_profiler SPUSBDataType | grep -c "iBridge"`
Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`

Result()
{
  if [ $? -eq 0 ];then 
  echo "\033[032m [PASS] RestoreM8 OK! \033[030m"
  fi
}  

while [ $M8 -eq 0 ]
do 
       while [ $Network -eq 0 ]
       do
          sleep 1
          Network=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
          echo "\033[031m [FAIL] 网络连接有问题，请检查！ \033[030m"
       done
       sleep 1
       static-ip-address -timeout 10
       sleep 1
       /usr/local/bin/restoreM8_QSMC_FATP.sh
       sleep 1
       M8=`system_profiler SPUSBDataType | grep -c "iBridge"`
done

Result
echo "\033[034m M8 OK，是否需要重新再次 Restore ? 如果需要请输入 [ 大写 Y ].. \033[030m"
read Input 
if [ $Input == "Y" ];then 
static-ip-address -timeout 10 ; sleep 1
/usr/local/bin/restoreM8_QSMC_FATP.sh
Result
fi

exit 0
      
      