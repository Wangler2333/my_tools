#!/bin/sh
#set -x
echo "\033[32m [Prompt] What kind of \033[31m[Bundle]\033[32m you want to delete , \033[31m[Test Bundle/TEST]\033[32m or \033[31m[CM Bundle/CM]\033[32m ? \033[30m"
read Bundle 
case $Bundle in 
*TEST* )
   Path="/Volumes/HedgehogRepo/DriveDuplicator/TestImages"
   echo "\033[32m [Prompt] Test Bundle List as Below... \033[30m"
   ls -l $Path | awk '{print$9}'
   echo ; echo "\033[32m [Prompt] Which one is you want to delete, and Pls input it then click 'enter' to continue... \033[30m" 
   read Input
   if [ `ls $Path | grep -c "$Input*"` -eq 1 ];then 
     BD=`ls $Path | grep "$Input*"`
     clisender rm -rf $Path/$BD ; sleep 1 ; echo "\033[32m [Pass] Deleted \033[30m"
     if [ `ls $Path | grep -c "$BD"` -eq 0 ];then 
       echo "\033[32m [Pass] Done ! \033[30m" ; exit 0
     else
       echo "\033[31m [Fail] And Pls check it ! \033[30m" ; exit 1
     fi 
   else
     N=`ls $Path | grep -c "$Input"`
     echo "\033[31m [Fail] Wrong Input , There Found $N Matched . Pls Check it ... \033[30m"   
   fi   
   #ls $Path | grep "$BD"
    
;;

*CM* )
   Path="/Volumes/HedgehogRepo/DriveDuplicator/CustomerImages"
   echo "\033[32m [Prompt] CM Bundle List as Below... \033[30m"
   ls -l $Path | awk '{print$9}'
   echo ; echo "\033[32m [Prompt] Which one is you want to delete, and Pls input it then click 'enter' to continue... \033[30m"
   read Input
   if [ `ls $Path | grep -c "$Input*"` -eq 1 ];then 
     BD=`ls $Path | grep "$Input*"`
     clisender rm -rf $Path/$BD ; sleep 1 ; echo "\033[32m [Pass] Deleted \033[30m"
     if [ `ls $Path | grep -c "$BD"` -eq 0 ];then 
        echo "\033[32m [Pass] Done ! \033[30m" ; exit 0
     else
        echo "\033[31m [Fail] And Pls check it ! \033[30m" ; exit 1
     fi
   else
     N=`ls $Path | grep -c "$Input"`
     echo "\033[31m [Fail] Wrong Input , There Found $N Matched . Pls Check it ... \033[30m"   
   fi 
   #ls $Path | grep "$BD" 
   
;;

* )
  echo "\033[31m [Fail] Wrong Input , Pls Enter \033[32m[TEST]\033[31m or\033[32m [CM]\033[31m ...  Try again ...\033[30m"    

esac   
     