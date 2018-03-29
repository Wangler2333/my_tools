#!/bin/bash

#
CAT()
{
cat /etc/passwd | head -$line
}
echo -n "Input the number of line:"
read line
limit=6
#
if [ $limit -gt $line ]
then
   while [ -n $line ]
   do 
     CAT
     break 2
   done
#
   echo -n "Continue?(answer yes/no):"
   read answer
   if [ $answer = 'yes' ]
   then 
     let line=line+1
     CAT
   fi
fi
exit 0          
