#!/bin/bash


en=$(ifconfig|grep -C 1 'ether ac:de:48:00:11:22'|grep '%en[0-9]'|cut -d'%' -f2|cut -d' ' -f1) && expect -c "spawn ssh -o StrictHostKeyChecking=no root@fe80::aede:48ff:fe33:4455%$en; expect -re \".*assword:.*\"; send \"alpine\r\"; expect -re \".*3.2\"; send \"controlbits write -o 166 -v incomplete\r\"; send \"controlbits write -o 240 -v incomplete\r\"; send \"controlbits write -o 176 -v incomplete\r\"; send \"controlbits write -o 138 -v incomplete\r\"; send \"controlbits write -o 137 -v incomplete\r\"; expect -re \".*3.2\"; send \"exit 0\r\"; interact"

