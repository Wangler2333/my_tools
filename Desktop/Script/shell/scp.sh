#!/bin/sh


# scp -r /Users/saseny/Desktop/TEST.zip gdlocal@172.23.171.193:/Users/gdlocal/Desktop/

echo "请输入要传输的文件路径:"
read source_path
echo "请输入目的用户名:"
read target_user
echo "请输入目的IP:"
read target_ip
echo "请输入目的路径:"
read target_path

echo $source_path,$target_user,$target_path,$target_ip