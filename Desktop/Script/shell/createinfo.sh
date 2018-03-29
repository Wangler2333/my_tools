#!/bin/sh
# Create by Saseny on 20170713
# For create a file with account info 

Dir=`dirname $0`
temp_file="/tmp/passwd.txt"
target_file="passwd.txt"
target_path=`pwd`

rm -rf "$target_path/$target_file"

# input info
echo "请输入(PDCA ip)"
read IpAddress
echo "请输入(PDCA 账号)"
read Username
echo "请输入(PDCA 密码)"
read -s Passwd
echo "请输入(电脑开机密码)"
read -s ComputerPasswd

echo "PDCAIP:"$IpAddress >> $temp_file
echo "PDCAAccount:"$Username >> $temp_file
echo "PDCAPassword:"$Passwd >> $temp_file
echo "HostPassword:"$ComputerPasswd >> $temp_file

openssl base64 -e -in "$temp_file" -out "$target_path/$target_file"

rm -rf $temp_file