#!/bin/bash

set -x

echo -n " Are you a student? "
read answer

if [ $answer = Y ]
   then 
     echo " Yes, I am a student "
   else
     echo " No, I am a teacher "
fi 
exit 0       
