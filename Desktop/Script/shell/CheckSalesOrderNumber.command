#!/bin/sh

SalesOrderNumber=`cat /Phoenix/Logs/state.txt | grep -c "SalesOrderNumber"`

if [ $SalesOrderNumber -eq 1 ];then
	echo "[PASS] SalesOrderNumber exist, continue Test !!!"
	exit 0
	
else
	echo "[FAIL] No SalesOrderNumber, abnormal process !!!"
	exit 1
	
fi