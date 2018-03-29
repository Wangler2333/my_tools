#!/bin/sh

Date=`date +%Y%m%d_%H%M%S`
SCRIPT_DIR=`dirname $0`
if [ -z $1 ];then
   logPath="$SCRIPT_DIR/DATALog" ; echo "[LogPath: $logPath]"
else
   logPath="$1" ; echo "[LogPath: $1]"
fi
resultPath="$SCRIPT_DIR/$Date.csv"
tmepPath="$SCRIPT_DIR/tmp"
  
Total=`ls -n $logPath | grep -c "Dec"`
allLogFinder=`ls $logPath`

echo "日期, 下载次数, 序列号, 下载总耗时, 测试Bundle下载时间, 测试BundelRestore带宽, 出货系统下载耗时, 出货系统下载带宽, 分区耗时, 线别, 站点, FixtureSlotID, 开始时间, 结束时间, 测试系统, 测试系统大小, 出货系统, 出货系统大小, WIP, PCIBridge, DCSD_Serial_Number, DriveDuplicator Host SN, PCIeSlot" >> $resultPath 

for oneLog in $allLogFinder
do
       mkdir -p $tmepPath
       cp -rf $logPath/$oneLog $tmepPath
       cd $tmepPath
       gunzip $oneLog
       
       logName=`echo $oneLog | awk -F '.gz' '{print$1}'`
       
       DateTime=`cat < $tmepPath/$logName | head -1 | awk -F '.' '{print$1}' | sed 's/\[//g' | awk '{print$1}'`
       BeginTime=`cat < $tmepPath/$logName | head -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
       EndTime=`cat < $tmepPath/$logName | tail -1 | awk -F '.' '{print$1}' | awk -F '[' '{print$2}'`
       PCIBridge=`cat < $tmepPath/$logName | grep "PCIBridge" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//'`
       PCIeSlot=`cat < $tmepPath/$logName | grep "PCIeSlot" | sed 's/.*= //' | sed 's/..$//' | sed 's/^.//' | head -1`
       DCSD_Serial_Number=`cat < $tmepPath/$logName | grep "DCSD Serial Number" | sed 's/.*= //' | sed 's/.$//'`
       FixtureSlotID=`cat < $tmepPath/$logName | grep "FixtureSlotID" | sed 's/.*= //' | sed 's/.$//'`
       SerialNumber=`cat < $tmepPath/$logName | grep "WIPSerialNumber" | head -1 | sed 's/.*= //' | sed 's/\;//'`
       HostSN=`cat < $tmepPath/$logName | grep "DriveDuplicator Host SN:" | sed 's/.*: //' | sed 's/\[//g' | sed 's/\]//g'`
       TestBundle=`cat < $tmepPath/$logName | grep "TestImages" | awk -F '.dmg' '{print$1}' | sed 's/.*\///'`
       WIP=`cat < $tmepPath/$logName | grep "WIPBarcod" | head -1 | awk -F ';' '{print$1}' | sed 's/.*\= //' | sed 's/"//g'`
       CMimage=`cat < $tmepPath/$logName | grep "CM image" | awk -F '.dmg]' '{print$1}' | sed 's/.*\[//'`
       TestBundleDownloadTime=`cat < $tmepPath/$logName | grep "Test Image Restore" | sed 's/.*= //'`
       CMbundleDownloadTime=`cat < $tmepPath/$logName | grep "CM Copy" | sed 's/.*= //' | head -1`       
       Overall=`cat < $tmepPath/$logName | grep "Overall" | sed 's/.*= //'`
       Partition=`cat < $tmepPath/$logName | grep "Partition =" | sed 's/.*= //'`
       TestBundleSize=`cat < $tmepPath/$logName | grep "Test Bundle size =" | sed 's/.*= //'`
       CMBundleSize=`cat < $tmepPath/$logName | grep "CM Bundle size =" | sed 's/.*= //'`
       ASR_bandwidth=`cat < $tmepPath/$logName | grep "ASR bandwidth =" | sed 's/.*= //'`
       CM_Copy_bandwitdth=`cat < $tmepPath/$logName | grep "CM Copy bandwitdth =" | sed 's/.*= //'`
       Line=`cat < $0 | grep "$HostSN" | awk '{print$2}'`
       Station=`cat < $0 | grep "$HostSN" | awk '{print$4}'`
       
       [ ! z $CMimage ] && CMimage="Did not Download"
       
       outPutMessage="$DateTime, $downLoadTimes, $SerialNumber, $Overall, $TestBundleDownloadTime, $ASR_bandwidth, $CMbundleDownloadTime, $CM_Copy_bandwitdth, $Partition, $Line, $Station, $FixtureSlotID, $BeginTime, $EndTime, $TestBundle, $TestBundleSize, $CMimage, $CMBundleSize, $WIP, $PCIBridge, $DCSD_Serial_Number, $HostSN, $PCIeSlot" 
       
       downLoadTimes=`ls $logPath | grep -c "$SerialNumber"`
       
       if [ $downLoadTimes -gt 1 ];then
           echo 1 >> $SCRIPT_DIR/count.log
           count=`cat < $SCRIPT_DIR/count.log | grep -c "1"`          
           if [ $count -eq $downLoadTimes ];then                          
             echo $outPutMessage >> $resultPath
             rm -rf $SCRIPT_DIR/count.log
           fi     
         else              
           echo $outPutMessage >> $resultPath 
       fi    
       
       let Total-=1       
       echo "[($Total)]"    
       [ $Total -eq 0 ] && echo "FINISHED!"
                 
       rm -rf $tmepPath
done    
rm -rf $SCRIPT_DIR/count.log
#sleep 3
#cd $SCRIPT_DIR
#sort -t, -k1n -o Modify_SWDL.csv $Date.csv
  
  
## 线别信息:站点:[拷贝机ID号] 
######################################################################
## F6-1FT-C1 : PRE-SWDL    : F5KR6048F693 F5KR604DF693 F5KS30HAF9VM
## F6-1FT-C1 : SW-DOWNLOAD : F5KR600HF693 F5KR6042F693
########################### 
## F6-1FT-D1 : PRE-SWDL    : F5KLQ02CF9VM F5KRR077F9VN F5KS304NF9VM
## F6-1FT-D1 : SW-DOWNLOAD : F5KLQ04DF9VN F5KR6056F693 F5KRR078F9VN
########################### 
## F6-2FT-F1 : PRE-SWDL    : F5KLQ04YF9VN F5KR603XF693 F5KSF03VF9VM
## F6-2FT-F1 : SW-DOWNLOAD : F5KLQ00TF693 F5KR60EXF9VM F5KRR06VF9VN
###########################
## F6-2FT-G1 : PRE-SWDL    : F5KLQ00ZF693 F5KR6046F693
## F6-2FT-G1 : SW-DOWNLOAD : F5KRR07BF9VN F5KR6041F693 F5KR604RF693
###########################
## RepairLine : Download : F5KRR06ZF9VN
#####################################################################  
