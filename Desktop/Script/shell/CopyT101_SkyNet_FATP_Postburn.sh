#!/bin/sh
#2014/07/11 Ver 1.1 standardize final log name
##############Init version 1.0
# Upload T101 summary csv to Skynet and archive local log
#Kaiser Yuan 2014/06/24

varInit()
{
LogServerIP=10.0.0.101
User=test
PASSWORD=test
LogPath=/Phoenix/tmp
DATE=`date +%Y%m%d`
T101LogFolder="/Phoenix/Logs/T101Cal_PostburnLog"
LocalArchived="/T101_Archived"
RecordFile=/Phoenix/tmp/LastFTP.txt

Product=""
Ypc=/AppleInternal/Diagnostics/Tools/ypc2
echo "Checking Product Name"
kvalue=`$Ypc -rk RPlt`
Product=`echo $kvalue |xxd -p -r|awk '{print toupper($0)}'`
SerialNumber=`cat /Phoenix/Logs/SerialNumber.txt`
Stage="FATP"
echo "System Platform is: $Product"

BuildStage=Proto3

}

archivedFile()
{
ping -t 1 $LogServerIP >/dev/null 2>&1
k=$?
if [ "$k" -ne 0 ]; then	
echo "WARNING: Can Not Find Any FTP Server"
exit 1
else

OIFS="$IFS"
IFS=$'\n'

if [ ! -d $LocalArchived ];then
echo "Create folder"
mkdir $LocalArchived
fi

for j in `find "$T101LogFolder" -type f -name "*Summary-*.csv"`;do
TestName=`echo $j | awk -F '/' '{print$(NF-2)}'`
FolderPath=`echo $j | sed 's/\/[^/]*$//'`
FolderName=`basename "$FolderPath"`

if [ ! -d $LocalArchived/$TestName ];then
mkdir $LocalArchived/$TestName
fi

cp -rf $FolderPath $LocalArchived/$TestName/$FolderName
done
IFS="$OIFS"

fi
}


ProcessT101Log()
{
OIFS="$IFS"
IFS=$'\n'
cd "$LocalArchived"/$TestName
for i in `find "$LocalArchived" -type f -name "*Summary-*.csv"`;do
TestName=`echo $i | awk -F '/' '{print$(NF-2)}'`
filename=`basename "$i"`
FolderPath=`echo $i | sed 's/\/[^/]*$//'`
FolderName=`basename "$FolderPath"`
zipfile="$FolderName".tgz
timeflag=`date +%Y_%m_%d_%H_%M_%S`

FinalLogName=SkyNet_"$Product"_"$Stage"_PostT101"$TestName"_"$SerialNumber"_"$timeflag".csv
FinalFolderName=SkyNet_"$Product"_"$Stage"_"$BuildStage"_"SerialNumber"_"$zipfile"

tar -czf $zipfile "$FolderName"

ping -t 1 $LogServerIP >/dev/null 2>&1
k=$?
if [ "$k" -ne 0 ]; then	
echo "WARNING: Can Not Find Any FTP Server"
exit 1
else
IP=`echo $LogServerIP`

	echo "Copy Logs To FTP Server"
  	(
      echo "user $User $PASSWORD"
      echo "mkdir SkyNet"  
      echo "cd SkyNet"  
      echo "mkdir $DATE"  
	  echo "! sleep 1 "
      echo "cd $DATE"     
      echo "put $i $FinalLogName"  #upload csv file
     # echo "cd /T101/Archived/$TestName"
      #echo "mkdir $DATE"  
	  #echo "! sleep 1 "
      #echo "cd $DATE" 
     # echo "put $zipfile $FinalFolderName"  #upload tgz log
    ) |ftp -n $IP
      echo "will delete all log files"
      mkdir $DATE
      mv "$LocalArchived"/$TestName/*.tgz "$LocalArchived"/$TestName/$DATE/
	  rm -rf "$FolderPath"   #delete origin log to prevent upload again
fi
done
IFS="$OIFS"
}

loggingRecord()
{
touch $RecordFile
echo "Last record time: " > $RecordFile
date +%Y%m%d_%H:%M:%S >> $RecordFile
}

#***********************************************************
#main script start#
#***********************************************************
varInit
archivedFile
ProcessT101Log
loggingRecord
rm -Rf $LocalArchived

