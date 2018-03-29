#!/bin/sh
# 开机启动脚本List

# 运行开始时间
#********************************************************************************
#echo >> /Users/saseny/Desktop/Stop/PID.txt
#echo "***********************" >> /Users/saseny/Desktop/Stop/PID.txt
#echo `date +%Y-%m-%d_%H:%M:%S` >> /Users/saseny/Desktop/Stop/PID.txt
#echo "***********************" >> /Users/saseny/Desktop/Stop/PID.txt 
#echo >> /Users/saseny/Desktop/Stop/PID.txt
#********************************************************************************


# jupyter server
#********************************************************************************
# Open server with 172.22.145.137:8888
open -a /Applications/iTerm2.app /Library/Scripts/MyScript/Net_Work_Running/jupyter.sh
sleep 2
#********************************************************************************


# python server
#********************************************************************************
# Open server with 172.22.145.137:8000
open -a /Applications/iTerm2.app /Library/Scripts/MyScript/Net_Work_Running/python.sh
sleep 2
#********************************************************************************



# Mysql server
#********************************************************************************
# Start mysql server 
mysql.server start
sleep 2
#********************************************************************************



# battery charge remind
#********************************************************************************
# Charge remind
nohup /Library/Scripts/MyScript/Net_Work_Running/charge_remind.py &
#********************************************************************************

# weather broadcast
#********************************************************************************
nohup /Library/Scripts/MyScript/Net_Work_Running/check_weather.py &
#********************************************************************************

nohup /Library/Scripts/MyScript/Net_Work_Running/GetTime.py &

# Log Collect
#********************************************************************************
#/Library/Scripts/MyScript/Net_Work_Running/PID.sh
#********************************************************************************


# kill terminal
#********************************************************************************
sleep 3
killall -m Terminal
#********************************************************************************