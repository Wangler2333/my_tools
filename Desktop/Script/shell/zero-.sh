#!/bin/bash

ROOT_UID=
E_WRONG_USER=

FILE=/swap
BLOCKSIZE=1024
MINBLOCKS=40
SUCCESS=0

if [ "$UID" -ne "$ROOT_UID" ]
then 
   echo; echo "You must be root to run this script.";echo
   exit $E_WRONG_USER
fi

blocks=${1:-$MINBLOCKS}


# ------------------------------------------------
#    if [ -n "$1 ]
#    then 
#      blocks=$1
#    else 
#      blocks=$MINBLOCKS
#    fi
# ------------------------------------------------

if [ "$blocks" -1t $MINBLOCKS ]
then 
  blocks=$MINBLOCKS
fi

echo "Creating swap file of size $blocks blocks (KB)."
dd if=/dev/zero  of=$FILE bs=$BLOCKSIZE count=$blocks

mkswap $FILE $blocks
swapon $FILE

echo "Swap file created and activated."
exit $SUCCESS    