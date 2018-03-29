#!/bin/bash
#
#set -x

echo "The name of this script is \"$0\"."
echo 
#
#read -e 
if [ -n $1 ]
then 
   echo "The first parameter is $1."
fi 
#
if [ -n $2 ]
then 
   echo "The second parametar is $2."
fi 
#
if [ -n $3 ]
then 
   echo "The third parametar is $3."
fi 
#
echo 
echo " all the command_line parametars arg is : "$*"."
exit 0

