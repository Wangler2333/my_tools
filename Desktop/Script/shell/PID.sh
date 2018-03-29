#!/bin/sh

sleep 5

# 运行开始时间
#********************************************************************************
echo >> /Users/saseny/Desktop/Stop/PID.txt
echo "***********************" >> /Users/saseny/Desktop/Stop/PID.txt
echo `date +%Y-%m-%d_%H:%M:%S` >> /Users/saseny/Desktop/Stop/PID.txt
echo "***********************" >> /Users/saseny/Desktop/Stop/PID.txt 
echo >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************


# jupyter server
#********************************************************************************
echo "--------------------------------------------------------------------" >> /Users/saseny/Desktop/Stop/PID.txt
ps -A | grep "jupyter-notebook" >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************



# python server
#********************************************************************************
echo "--------------------------------------------------------------------" >> /Users/saseny/Desktop/Stop/PID.txt
ps -A | grep "python manage.py runserver 172.22.145.137:8000" >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************



# Mysql server
#********************************************************************************
echo "--------------------------------------------------------------------" >> /Users/saseny/Desktop/Stop/PID.txt
ps -A | grep "mysql" >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************



# battery charge remind
#********************************************************************************
echo "--------------------------------------------------------------------" >> /Users/saseny/Desktop/Stop/PID.txt
ps -A | grep "/Library/Scripts/MyScript/Net_Work_Running/charge_remind.py" >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************