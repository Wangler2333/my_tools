#!/bin/sh
#set -x

Dir=`dirname $0`
mkdir -p $Dir/OUT
DATE=`date +%m-%d`
TIME=`date +%T`
ErrorCodeFile="$Dir/DefaultFile/ErrorCode_Runin.txt"
radarFile="$Dir/DefaultFile/Radar.txt"
reportFile="$Dir/OUT/$DATE.csv"
Location=Runin

Output()
{
  echo "$DATE,$SerialNumber,$UnitNumber,$Config,$Location,$FailMessage,$radarNo,$Remark" >> $reportFile
}  

CheckCrash()
{
   CrashStates=`ls $tempPath/$FolderName/_LIBRARY_LOGS/Logs/DiagnosticReports | grep -c "PhoenixCE Crash"`
   if [ $CrashStates -gt 0 ];then 
     echo "[$SerialNumber] Have Phoenix Crash. Pls Check and Input crash info:"
     read Crash
     FailMessage=$Crash
     Output
   fi    
}   

ManualCheck()
{
#  Hang & KP
  echo "Whether Hang or KP in Test Process ? Yes (input Fail Message) / No (input n)..."
  read input
  case $input in 
    *n*)
      ;;
    *)
      FailMessage=$input
      Output ;;
  esac      
}

CheckPASS()
{
 iD=`cat < $processlogPath | grep "FAIL-UPDA" | awk -F '"' '{print$16}'`
 if [ $iD -eq "0" ];then
   FailMessage="PASS" 
   echo $FailMessage 
   Output
 else        
   CheckRetryPass    
fi
}       

CheckRetryPass()
{
# check ERROR Fail or Retry Passed
# Delete 'Unknow' Row
sed -i "" '/Unknown/d' $Dir/DefaultFile/ERROR.txt
ErrorCodeFail=`cat < $Dir/DefaultFile/ERROR.txt | awk '{print$2}'`

#ABC=`cat < $Dir/DefaultFile/ERROR.txt`
#[ -z $ABC ] && FailMessage="PASS"
for r in $ErrorCodeFail
do 
  volue_=`cat < $Dir/DefaultFile/ERROR.txt | grep "$r" | grep -c "Passed on Retry"`
  if [ $volue_ -eq 0 ];then 
   FailMessage=`cat < $Dir/DefaultFile/ERROR.txt | grep "$r"`
   #radarNo=`cat < $Dir/DefaultFile/Radar.txt | grep "$r" | sed 's/.*: //'`
   Output
  fi   
done

rm -rf $Dir/DefaultFile/ERROR.txt
}


#**********************************************************************************************

echo "Date,Serial Number,Unit Number,Config,Location,Error Code,Radar Number,Remark(Bundle)" >> $reportFile

OverallLog=`find $Dir -type f -iname *.tgz -print | wc -l | sed 's/\ //g'`
tempPath="$Dir/TEMP"


TotalLog=0
    
   
   for i in `find $Dir -type f -iname *.tgz -print`; do 
   
      TotalLog=`expr $TotalLog + 1`
      echo "Processing log [$TotalLog / $OverallLog]"
        
        FolderName=`echo $i | awk -F '/' '{print$NF}' | awk -F '.' '{print$1}' | sed 's/.*C02/C02/'`
        SerialNumber=`echo $FolderName | awk -F '_' '{print$1}'`
                    
           mkdir -p $tempPath 
           cd $tempPath          
           tar -zxvf $i &>/dev/null

           processlogPath="$tempPath/$FolderName/_PHOENIX_LOGS/Logs/processlog.plog"
           
           UnitNumber=`cat < $Dir/DefaultFile/Unitsinfo.txt | grep "$SerialNumber" | awk '{print$5}'`
           Config=`cat < $Dir/DefaultFile/Unitsinfo.txt | grep "$SerialNumber" | awk '{print$4}'`
           Remark=`cat < $processlogPath | grep "DTIVersion" | tail -1 | sed 's/.*Bundle=//' | sed 's/.*Bundle=//' | awk -F ',' '{print$1}' | sed 's/"//g'`
        
        UnitStates=`echo $i | grep -c "FAIL"`
        if [ `echo $i | grep -c "FAIL"` -eq 1 ];then

           #----------------------------------------------------------------------------------------------------# 
           $Dir/DefaultFile/ReadDTIinfo.sh $tempPath/$FolderName/_PHOENIX_LOGS/Logs/processlog.plog $Dir/OUT/DTIinfo.csv
           #----------------------------------------------------------------------------------------------------# 
           #ErrorCode1=`cat < $processlogPath | grep "FAIL-UPDA" | awk -F '"' '{print$20,$16,$22,$84}' | sort -u`
           #----------------------------------------------------------------------------------------------------# 
           #echo $ErrorCode1
           cat < $processlogPath | grep "FAIL-UPDA" | awk -F '"' '{print$20,$16,$22,$84}' | sort -u | sed 's/,//g' >> $Dir/DefaultFile/ERROR.txt       # ???
           #sleep 10
           #----------------------------------------------------------------------------------------------------#      
           CheckRetryPass
         elif [ `echo $i | grep -c "PASS"` -eq 1 ];then
           FailMessage=PASS
           Output          
         fi  
         #CheckCrash  
         rm -rf $tempPath/$FolderName  
   done
   rm -rf $tempPath