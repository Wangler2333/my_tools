#!/bin/bash

#
echo " decimal  hex  character "
for ((i=1;i<=36;i++))
  do
    echo $i | awk '{printf("%3d   %2x   %c\n",$1,$1,$1)}'
  done
exit 0    
