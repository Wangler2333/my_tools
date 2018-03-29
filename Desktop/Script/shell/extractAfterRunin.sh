#!/bin/bash
set -x

	logfile="/Phoenix/Logs/processlog.plog"
	resultFile="/Phoenix/Logs/AfterRunin.txt"

	tmpStr=$(grep PHNX-INFO $logfile  | grep PhoenixOS | tail -1)

	echo $tmpStr | awk -F, ' 
		BEGIN 	{  
		}{ for( i=1; i<(NF+1); i++){
			#print $i ":" length($i);
			if( $i ~ /Bundle/ ){
				bundleName=substr($i,9,length($i)-9);
			}
			if( $i ~ /ControlBuild/ ){
				controlBuild=substr($i,15,length($i)-15);
			}
			if( $i ~ /WIPNo/ ){
				wipNo=$i;
				marketNo=substr(wipNo,20,length($i)-20);
			}
		 }
		}
		END{ print "Market Number: " marketNo "\nControl Build: " controlBuild "\nBundle Name  : " bundleName;
		}' > $resultFile

	exit 0
