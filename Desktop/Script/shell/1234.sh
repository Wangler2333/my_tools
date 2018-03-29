#!/bin/bash
#
variable1_=$1_
critical_argument01=$variable1_
variable1=${variable1_/_/}
#
if [ -z $1 ]
then 
  exit $MISSING_PARAM
fi 
exit 0  