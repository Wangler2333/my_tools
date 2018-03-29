#!/bin/sh

SCRIPT_DIR=`dirname $0`
passWord="Saseny_Zhou"
Times=0
MaxTimes=10

PASSWord=`echo -n $passWord | shasum -a 256 | awk -F '-' '{print$1}' | sed 's/\ //g'`       
echo "\033[032m请输入操作代码，对文件编码加密(Code),对加密文件解码(Decode):\033[030m"
  while (True)
  do 
    read Enter
    if [ $Enter == "Code" ];then 
      echo "\033[032m请拖入要编码的文件路径名:\033[030m"
      read inPutFile
      suffix=`echo $inPutFile | awk -F '.' '{print$2}'`
      outPut="$SCRIPT_DIR/$suffix.txt" 
      echo "\033[032m进行文件编码...!\033[030m"
      openssl base64 -in $inPutFile -out $outPut -aes-128-cbc -k $PASSWord    #  Code
      if [ $? -eq 0 ];then 
         echo "\033[032m[PASS]编码完成!输出路径:$outPut\033[030m"
      else
         echo "\033[031m[FAIL]编码失败!\033[030m"
      fi
      exit 0
    elif [ $Enter == "Decode" ];then 
      echo "\033[032m请拖入要解码的文件路径名:\033[030m"
      read inPutFile
      echo "\033[032m请输入输出文件名+后缀名:\033[030m"
      read suffix
      outPut="$SCRIPT_DIR/$suffix"
      echo "\033[032m进行文件解码...!\033[030m" 
      openssl base64 -d -in $inPutFile -out $outPut -aes-128-cbc -k $PASSWord   #  Decode 
      if [ $? -eq 0 ];then 
         echo "\033[032m[PASS]解码完成!输出路径:$outPut\033[030m"
      else
         echo "\033[031m[FAIL]解码失败!\033[030m"
      fi
      exit 0
    else
      let CurrentTimes=Times+2
      echo 
      echo "\033[031m第[$CurrentTimes]次,最大次数限制:[$MaxTimes 次].\033[030m"
      echo "\033[032m输入错误，请重新输入(Code or Decode):\033[030m"
    fi   
    let Times+=1  
    if [ $Times -eq $MaxTimes ]; then
      echo  
      echo "\033[031m错误输入次数达到最大限制
      :[$MaxTimes],脚本运行结束!\033[030m" ; exit 1
    fi  
  done