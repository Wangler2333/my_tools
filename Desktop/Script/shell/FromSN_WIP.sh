#!/bin/sh
#set -x
## 根据SN 搜集WIP
Path="/Users/bundle/Downloads/DOWN"
Host="LL_DOE"


Log=`ls $Path`

for A in $Log 
do 

    SN=`echo $A | awk -F '_' '{print$1}'`
    mkdir -p /Users/bundle/Downloads/tmp
    cp -rf $Path/$A /Users/bundle/Downloads/tmp
    
    cd /Users/bundle/Downloads/tmp 
    gunzip $A
    
    Name=`echo $A | awk -F '.gz' '{print$1}'`    
    WIP1=`cat < /Users/bundle/Downloads/tmp/$Name | grep "WIPBarcod" | head -1 | awk -F ';' '{print$1}' | sed 's/.*\= //'`     
    IFS='"'   
    
    WIP=`echo $WIP1 | sed 's/.*\ //'`
    EX=`cat < /Users/bundle/Downloads/$Host.txt`
    
    case $EX in
    *$WIP*)
    echo "WIP Exist!"
    ;;
    *)
    echo $WIP >> /Users/bundle/Downloads/$Host.txt 
    ;;
    esac
    rm -rf /Users/bundle/Downloads/tmp
    
done

echo "Total:[`cat < /Users/bundle/Downloads/$Host.txt | grep -c "+"`]"
    
    
    
