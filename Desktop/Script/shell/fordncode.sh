#!/bin/sh

Password="~Saseny"

echo "请输入需要加密的文件路径:"
read in_file

echo "请输入输出文件名与路径:"
read out_file

openssl base64 -d -in $in_file -out $out_file -k $Password
