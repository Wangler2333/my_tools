#!/bin/sh
# For Python others model update 

CycleTimes=1
count=0

echo "-->> 请输入电脑开机密码:"
read -s password
if [ -z $password ];then
   echo "-->> 未输入密码，请重试..."
   exit 1
fi

Dir=`dirname $0`

if [ ! -f $Dir/pyhtonModel.txt ];then
   echo "-->> 默认文件不存在. 请检查 [$Dir/pyhtonModel.txt] ..."
   exit 1
fi
allModel=`cat < $Dir/pyhtonModel.txt | awk '{print$1}'`

while [ $count -lt $CycleTimes ]
do 
    count = $count + 1 
    for i in $allModel
    do 
        pip install $i   
        if [ $? -eq 1 ];then        
            echo "[The 1 Install FAIL] -- (Retry) -->> pip install $i" >> $Dir/PassFialCount.txt
            pip install $i      
            if [ $? -eq 1 ];then
                echo "[The 2 Install FAIL] -- (Retry) -->> pip install $i" >> $Dir/PassFialCount.txt
                Time=3
                expect -c "set timeout 2;spawn sudo pip install $i ; expect -re \".*password*\";send \"$password\r\";expect -re \"$\";interact"             
            else
                 echo "[The 2 Install PASS] -- (PASS) -->> pip install $i" >> $Dir/PassFialCount.txt    
            fi   
        else
            echo "[The 2 Install PASS] -- (PASS) -->> pip install $i" >> $Dir/PassFialCount.txt     
        fi  
    done   
done      
        
        
   


 
