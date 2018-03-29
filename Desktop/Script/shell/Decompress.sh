#!/bin/sh

nameCheck=`echo $1 | awk -F '.' '{print$NF}'`
    
case $nameCheck in 

   *tgz*)
     tar -zxvf $1   ;;
  
   *gz*)
     gunzip $1      ;;

   *zip*)
     unzip $1  ;;
  
   *tar*)
     tar xvf $1  ;;

   *bz2*)
     bzip2 -d $1  ;;
  
   *rar*)
     rar x $1  ;;

   *)
     echo "Unknown file format!"
     exit 1    
esac      
exit 0         