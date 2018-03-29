#!/bin/sh

if [ ! -f "/Phoenix/Logs/ADPStatus.txt" ]; then
	echo "Unit first power on"
	ADPStatus=`/TE_Support/Scripts/Test_Process/ypc2 -rdk ACIN | awk '{print int($0)}'`
		if [ $ADPStatus -eq 0 ];then
			echo "Unit disconnected with Adapter"
			echo "${ADPStatus}" > "/Phoenix/Logs/ADPStatus.txt"
		else
			echo "Unit connected with Adapter"
			echo -e "\033[31m========================="
			echo -e "\033[31m*****   ***   *****  *   "
			echo -e "\033[31m*      *   *    *    *   "
			echo -e "\033[31m****   *****    *    *   "
			echo -e "\033[31m*      *   *    *    *   "
			echo -e "\033[31m*      *   *  *****  ****"
			echo -e "\033[31m========================="
			echo ""
			echo "按Y键关闭Unit[Y]:"
			
			read continue
			while [ $continue != Y ]; do
				echo "请输入Y然后手动重启电脑[Y]:"
				read continue;
			done
			if [ $continue == Y ]; then
				echo "Shut down unit......"
				shutdown -h now
				exit 1
			fi
		fi
	else
		echo "Unit has been powered on before"
fi