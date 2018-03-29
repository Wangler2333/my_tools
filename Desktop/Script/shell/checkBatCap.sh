#!/bin/bash

################################################################################
# Description: Check Battery Capacity is within expect range                   #
#------------------------------------------------------------------------------#
# Version:     1.0.0 (Initial release)                                         #
# Version:     1.0.1 (Get Battery info with access SMC Key)                    #
# Author:      Felix Yuan                                                      #
# Date:        Sep 21, 2010                                                    # 
################################################################################

    # Color for echo
    redColor='\E[31;47m'
    blueColor='\E[34;47m'
    yellowColor='\E[32;47m'
    defaultColor='\E[00;00m'
   
    loLimiter=20
    hiLimiter=85
   
    # Usage
    usage(){
       echo "Usage: checkBatCap [-u UpperLimiter] [-l LowerLimiter]"
    }
   
    while getopts ":hu:l:" option
    do
        case $option in
            u) hiLimiter=$OPTARG;;
            l) loLimiter=$OPTARG;;
            h) usage& 
               exit 0;;
            *) echo $OPTARG is an unrecognized option
               exit 0;;
        esac
    done

    if [ $hiLimiter -lt $loLimiter ]; then
        echo "ERROR: Upper Limiter is lower than Low Limiter"
        exit 1
    fi
    printf "Check Battery Capacity is between $loLimiter%% and $hiLimiter%%: \n"
    
    Ypc2Tool="/AppleInternal/Diagnostics/Tools/ypc2"
    Ypc2maxCap=$($Ypc2Tool -r -k B0FC -d | awk -F '.' '{print $1}')
    Ypc2CurCap=$($Ypc2Tool -r -k B0RM -d | awk -F '.' '{print $1}')
    Ypc2perCap=$(expr $Ypc2CurCap "*" 100 / $Ypc2maxCap)
      
  	printf "Yp2c: $Ypc2perCap%%\n"    
    
    currentCap=$(ioreg -l w0 | grep CurrentCapacity | awk '{print $NF}')
    maxCap=$(ioreg -l w0 | grep MaxCapacity | awk '{print $NF}')
    IoperCap=$(expr $currentCap "*" 100 / $maxCap)
    
    printf "Ioreg: $IoperCap%%\n"
    
    
    if [[ $Ypc2perCap -ge $loLimiter  &&  $Ypc2perCap -le $hiLimiter ]]; then
        printf "$Ypc2perCap%% PASS\n"
        printf "MaxCap: $Ypc2maxCap\n"
        printf "CurCap: $Ypc2CurCap\n"
        exit 0
    else
        printf "$Ypc2perCap%% FAIL\n"
        printf "MaxCap: $Ypc2maxCap\n"
        printf "CurCap: $Ypc2CurCap\n"
        exit 1
    fi
   