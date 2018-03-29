#!/bin/sh

SearchDir=`dirname $0`
DATE=`date +%Y%m%d@%H%M%S`
TargetDir="$SearchDir/$DATE.csv"
TmpDir="$SearchDir/temp"
FileFormat="tgz"
B=3600   # 时间计算

## 搜索参数 ##
startParameter="CM_Bundle_Verify" 
endParameter="MSD.ntab"

echo "Serial Numebr, Test Times, CPU, Memory, SSD, Contry, Time Start, Time End, Time Left(Hour)" >> $TargetDir

TotalLog=0

mkdir -p $TmpDir
cd $TmpDir

OverallLog=`find $SearchDir -type f -iname *.tgz -print | wc -l | sed 's/\ //g'`

    for i in `find $SearchDir -type f -iname *.tgz -print`; do
         TotalLog=`expr $TotalLog + 1`
		 echo "Processing log [$TotalLog / $OverallLog]"
		 
		 FolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | sed 's/.*C02/C02/'`
		 SerialNumber=`echo $FolderName | awk -F '_' '{print$1}'`
		 
		 tar -xzf $i &>/dev/null
		 
		 Storage=`cat < $TmpDir/$FolderName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Storage" | awk -F '=' '{print$2}' | awk -F '&' '{print$1}' | sed 's/"//g'`
		 GenuineIntelsource=`cat < $TmpDir/$FolderName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "GenuineIntel" | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`
		 Memory=`cat < $TmpDir/$FolderName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Memory" | awk -F '=' '{print$2}' | awk -F '&' '{print$1}' | sed 's/"//g'`
		 Keyboard=`cat < $TmpDir/$FolderName/_PHOENIX_CONFIGURATION/Configuration/configExpected.txt | grep "Keyboard" | tail -1 | awk -F '=' '{print$3}' | awk -F '&' '{print$1}' | sed 's/"//g'`


		 A=1000
		 GenuineIntel=`echo "scale=1;$GenuineIntelsource/$A" |bc`		
		 
		 ## Time Calculate
         
         TestTimes=`find $SearchDir -type f -iname *.tgz -print | grep -c "$SerialNumber"`
         if [ $TestTimes -gt 1 ];then
            echo 1 >> /tmp/count.log
            count=`cat < /tmp/count.log | grep -c "1"`
            if [ $count -eq $TestTimes ];then
               echo "$SerialNumber,$TestTimes,$GenuineIntel,$Memory,$Storage,$Keyboard,$run_inBeginTime,$run_inEndTime,$timeleft" >> $TargetDir 
               rm -rf /tmp/count.log
            fi
          else  
          
            run_inBeginTime=`cat < $TmpDir/$FolderName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "$startParameter" | head -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
            run_inEndTime=`cat < $TmpDir/$FolderName/_PHOENIX_LOGS_PROCESSLOG.PLOG/processlog.plog | grep "$endParameter" | tail -1 | awk -F ',' '{print$2}' | sed 's/.*=//' | sed 's/"//g'`
          
          
            StartTimeSample=`date -j -f date -j -f "%Y/%m/%d %T" "$run_inBeginTime" +"%s"`
            EndTimeSample=`date -j -f date -j -f "%Y/%m/%d %T" "$run_inEndTime" +"%s"`
            TimeUsed=`expr ${EndTimeSample} - ${StartTimeSample}`	
            timeleft=`echo "scale=2;$TimeUsed/$B" |bc`
   
            echo "$SerialNumber,$TestTimes,$GenuineIntel,$Memory,$Storage,$Keyboard,$run_inBeginTime,$run_inEndTime,$timeleft" >> $TargetDir
         fi  
         rm -rf /$TmpDir/$FolderName

done       
		 
		 
echo ; echo 
echo "\033[32m===================================================\033[m"
echo "\033[32m           ****   *****  *   *  *****              \033[m"
echo "\033[32m           *   *  *   *  **  *  *                  \033[m"
echo "\033[32m           *   *  *   *  * * *  *****              \033[m"
echo "\033[32m           *   *  *   *  *  **  *                  \033[m"
echo "\033[32m           ****   *****  *   *  *****              \033[m"
echo "\033[32m===================================================\033[m"
echo "\033[32m       Total Process [$TotalLog] Data			     \033[m"
echo "\033[32m===================================================\033[m"	
echo ; echo		 