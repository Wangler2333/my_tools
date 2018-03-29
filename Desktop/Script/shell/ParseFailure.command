#!/bin/sh
#*******************************************************
#
# Main 
# 
# @ HT Law , 10 June 2014
#*******************************************************
# 16 June:
# - Dynamic way to parse out the field base on array
#   to recognize both EFI and OS type error.
# 11 July: 
# - Get the line array delimited by ';', to receive correct fail name 
# - Fix bug where output correct error code for commandline
# - Add header
# - Reset format to suit for Skynet
# - Time Conversion to format yyyy-mm-dd
# 12 July:
# - Fix bugs for logging retry.
# - Fix all description and test name w/o delimiter ,
# 16 Sept - HQ Zhou:
# - Add cat /Phoenix/Logs/SkyNet_WiPAS_Error_Log.csv >> "$ResultFile".
#*******************************************************
convertTimeStamp()
{
case "${Env[$n]}" in
"OS" )
ymd=`echo ${TOF[$n]} | awk -F'_' '{print$1}'`
hms=`echo ${TOF[$n]} | awk -F'_' '{print$NF}'`
year=`echo $ymd | awk -F'-' '{print$NF}'`
month=`echo $ymd | awk -F'-' '{print$1}'`
tdate=`echo $ymd | awk -F'-' '{print$2}'`
TOF[$n]=`echo "$year-$month-$tdate"_"$hms"`
;;
"EFI" )
TOF[$n]=`echo ${TOF[$n]} | sed 's/\//-/g'`
;;
esac
#echo ${TOF[$n]}
}

todayDate=`date +%Y/%m/%d`
pLog="/Phoenix/Logs/processlog.plog"
temp="/private/var/root/Desktop/temp.txt"
Result="/private/var/root/Desktop/"
TestStage=$1

#pLog=`dirname $0`/processlog.plog
#temp=`dirname $0`/temp.txt
#Result=`dirname $0`/



Product=""
Ypc=/AppleInternal/Diagnostics/Tools/ypc2
echo "Checking Product Name"
kvalue=`$Ypc -rk RPlt`
Product=`echo $kvalue |xxd -p -r|awk '{print toupper($0)}'`
echo "System Platform is: $Product"
BuildStage=`cat /Phoenix/Tables/BuildStage.txt | sed 's/.*=//'`
FATP=FATP
TimeStamp=`date +%Y_%m_%d_%H_%M_%S`
echo $BuildStage

if [ ! -f $temp ];then
touch $temp
fi

if [ -f /Phoenix/Logs/SerialNumber.txt ];then
Sernum=`cat /Phoenix/Logs/SerialNumber.txt`
echo $Sernum
else
Sernum=`cat $pLog | grep "WIP scanned=" | awk -F'"' '{print $(NF-1)}' | tail -1 | sed 's/+.*//'`
echo $Sernum
fi

ResultFile="$Result""SkyNet"_"$Product"_"$FATP"_"$TestStage"_"$Sernum"_"$TimeStamp.csv"

echo $ResultFile

cat $pLog | grep "FAIL-UPDA" | sed 's/\",/@/g' | sed 's/"//g' | sed 's/\ /_/g' > $temp

#echo "***************F A I L***********************\n\n" > "$ResultFile"
#printf "SerialNumber,TOF,FailStage#FailCycle,Test ID,TestName,Error Message" >> "$ResultFile"
printf "SerialNumber,TOF,FailStage#FailCycle,Test Group,Test ID,TestName,Error Message" >> "$ResultFile"

n=0
while read line
do
n=`expr $n + 1`
line=($line)

IFS='@'
for elem in ${line[@]};do
#echo ${elem[@]}
case $elem in
*"Command_Package_Name"* )
TestPackage[$n]=`echo $elem | awk -F'=' '{print $2}' | sed 's/,/;/g'`;;
*"Extended_Code"* )
Testid[$n]=`echo $elem | awk -F'=' '{print $2}' | sed 's/,/;/g'`;;
*"Extended_Name"* )
TestName[$n]=`echo $elem | awk -F'=' '{for(i=2;i<=NF;i++){printf $i}}' | sed 's/,/;/g'`;;
*"Stage_Name"* )
Stage[$n]=`echo $elem | awk -F'=' '{print $2}' | sed 's/_//g'`;;
*"Result_Msg"* )
Failmsg[$n]=`echo $elem | awk -F'=' '{print $2}' | sed 's/,/;/g'`;;
*"Matrix_PC"* )
Loop[$n]=`echo $elem | awk -F'=' '{print $2}'`;;
*"Overridden_Mode"* )
Status[$n]=`echo $elem | awk -F'=' '{print $2}'`;;
*"Environment"* )
Env[$n]=`echo $elem | awk -F'=' '{print $2}'`;;
*"TOF"* )
TOF[$n]=`echo $elem | awk -F'=' '{print $2}'`
convertTimeStamp
;;
esac

done
#IFS=$OLDIFS

case "${TestPackage[$n]}" in
*"Core.Check.Config"* | *"Util.Exec.Shell"* | *"Comm."* | "Query."* )
key[$n]="${Sernum},${TOF[$n]},${Stage[$n]}#${Loop[$n]},${TestPackage[$n]} Test,${Env[$n]} ${TestPackage[$n]},${TestName[$n]},${Failmsg[$n]},${Status[$n]}"
;;
* )
key[$n]="${Sernum},${TOF[$n]},${Stage[$n]}#${Loop[$n]},${TestPackage[$n]} Test,${Env[$n]} ${TestPackage[$n]} #${Testid[$n]},${TestName[$n]},${Failmsg[$n]},${Status[$n]}"
;;
esac

done < $temp

tot_Fail=${#key[@]}
n=0
while [ $n -le $tot_Fail ];
do

#echo "Status is [${Status[$n]}]"
if [ "${TestName[$n]}" == "${TestName[`expr $n + 1`]}" ] && [ "${Status[`expr $n + 1`]}" == "Passed_on_Retry" ] ;then
echo "Skip logging record"
elif [ "${Status[$n]}" == "Passed_on_Retry" ] || [ "${Status[$n]}" == "Rework Override" ];then
echo "Skip logging record"
else
echo ${key[$n]} | sed 's/_/\ /g' >> "$ResultFile"
fi
n=`expr $n + 1`
done

cat /Phoenix/Logs/SkyNet_WiPAS_Error_Log.csv >> "$ResultFile"
cat /Phoenix/Logs/SkyNet_Euphony_Error_Log.csv >> "$ResultFile"
#IFS=$OLDIFS
#get=`cat "$ResultFile" | sed 's/;/,/g'`
#echo $get > "$ResultFile"
#echo "\n\nTotal Failures = [ $Total ]" >> "$ResultFile"
rm -rf $temp
cp -rf "$ResultFile" /Phoenix/Logs
cp -rf "$ResultFile" /Phoenix/tmp
