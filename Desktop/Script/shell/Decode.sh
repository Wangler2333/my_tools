#!/bin/sh

Dir=`dirname $0`
temp_file="/tmp/passwd.txt"
target_file="passwd.txt"
target_path=`pwd`

openssl base64 -d -in "$target_path/$target_file" -out "$temp_file"
