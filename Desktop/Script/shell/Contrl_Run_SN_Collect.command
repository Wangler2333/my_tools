#!/bin/sh

## 收集 Control Run WIP ，不写入重复值

Control_Name="5-11.26.0E2"

Path=`echo $0 | awk -F 'Contrl_Run_SN_Collect.command' '{print$1}'`
AB=1
[ `cat < $Path/$Control_Name.txt | grep -c "WIP"` -eq 0 ] && echo "Control_Run_WIP" >> $Path/$Control_Name.txt

while [ $AB -eq 1 ]
do 

read SN
Write=`cat < $Path/$Control_Name.txt`
Number=`cat < $Path/$Control_Name.txt | grep -c "+"`
#Number=`cat -n $Path/$Control_Name.txt | awk '{print$1}' | tail -1`

case $Write in
*$SN* )
    echo "\033[031m[FAIL] WIP Exist !\033[030m" 
    ;; 
*)
    let Number=$Number+1
    #let Number=$Number-1
    echo "\033[032m[PASS][$Number]\033[030m"
    echo $SN >> $Path/$Control_Name.txt
    ;;
esac    
    
done      

