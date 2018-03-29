#!/bin/sh

# This script is to get APPLE SSD PE CYCLE failed data
# Written by Kaiser Yuan
# 2015/04/08
# Usage: 
#1.copy the command to the log folder
#2.Open Terminal,cd to the log folder, 
#3.run ./Parse_SSD_PE_Cycle.sh.command
# -------------------rev 1.0-------------------
#Save a csv file for each log at $Inputdir/result

Product="J11x"
Stage="FATP"
INPUTDIR=`pwd`

#LIST FILE
cd $INPUTDIR
ls *.tgz  > /tmp/list.log
if [ ! -e /tmp/List.log ]
then echo "/tmp/List.log is NOT existed!..."; exit -1
fi

# begin of parse each log
cat /tmp/list.log | while read zipfileline
do
echo zipfileline=$zipfileline
#echo $zipfileline
tar -xvf $zipfileline *processlog.plog >& /tmp/output.log    #exact the tgz file

#Processlog.plog
Logpath=$(cat /tmp/output.log | awk -F\  '{ printf $2 }')
#echo Logpath=$Logpath

# begin of parsing the processlog.plog 
output()
{
        out=$1
		echo -n $out >> $OUTPUTFILE
		echo -n "," >> $OUTPUTFILE
		
}
 
	if [[ -s /Phoenix/Logs/SerialNumber.txt ]];then
		UnitSN=`cat /Phoenix/Logs/SerialNumber.txt`
     	else
		UnitSN=`echo $zipfileline| awk -F_ '{ printf $1 }' `
   fi


if [[ -s $Logpath ]];then
	
     echo "Starting Log Collect SSD PE Info"
	else
	  echo "Can not find log file"
	 exit 1
fi

mkdir -p $INPUTDIR/result

#output "way 00" PE cycles, change the string can check other failures
cat $Logpath | grep "ERROR: 1 GBB > 0" | awk -F\, '{print $2 $NF}' >> $INPUTDIR/result/"$Product"_"$Stage"-"$UnitSN".csv

next
# end of all log
done

# clear temprary directory
find ./ -name "*_??" -exec rm -rf {} \;
rm /tmp/*.log

echo "Job is Done!"

exit 0