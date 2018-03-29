#/bin/bash
# History:
# 2016/07/20	Saseny	

#read -p "Please input (Y/N): " yn
#[ "${yn}" == "Y" -o "${yn}" == "y" ] && echo "OK, continue" && do
#[ "${yn}" == "N" -o "${yn}" == "n" ] && echo "Oh, interrupt!" && exit 0
#echo "I don't know what your choice is" && exit 0
#read - e OK, continue
#done

echo " "
echo " "
echo " "
echo " 请选择正确的###此###仅用于### "
echo " "
echo " "
echo " "
echo "    #              #             #             # # # #           ##      #        #    "
echo "    #  #         # #            #  #              #              # #     #        #    "
echo "    #    #     #   #           #    #             #              #  #    #        #    "
echo "    #      # #     #          # #### #            #              #   #   #        #    "
echo "    #       #      #          #      #            #              #    #  #        #    "
echo "    #              #          #      #            #              #     # #             "
echo "    #              #          #      #         # # # #           #      ##        @    "
echo " "
echo " "
echo " "
echo " 请选择是否继续［ Y 或者 N ］－ (请使用大写) "
echo " "
echo " "
read -e continue
while [ $continue != Y ] && [ $continue != N ]; do
     echo " 是否继续［ Y 或者 N ］"
     read -e continue;
     done
if [ $continue != Y ]; then
     echo " "
     echo " "
     echo " 运行停止 ！ "
     echo " "   
     echo " "
     exit
fi    

echo " "
echo " "
echo " "
   
    
echo  "  ###########       #       #       #                                             "
echo  "  #         #       #      #        #                                             "
echo  "  #         #       #     #         #                                             "
echo  "  #         #       #    #          #                                 #           "
echo  "  #         #       #   #           #              #####################          "
echo  "  #         #       # # #           #              ######################         "
echo  "  #         #       #    #          #              #####################          "
echo  "  #         #       #     #         #                                 #           "
echo  "  #         #       #      #        #                                             "
echo  "  #         #       #       #                                                     "
echo  "  ###########       #        #      @                                             "


echo " "
echo " "
echo " "
#echo " 请选择是否继续［ Y 或者 N ］－ (请使用大写) "
#read -e continue
#while [ $continue != Y ] && [ $continue != N ]; do
#     echo " 是否继续［ Y 或者 N ］"
#     read -e continue;
#     done
#if [ $continue != Y ]; then
#     echo " "
#     echo " "
#     echo " 运行停止 ！ "
#     echo " "   
#     echo " "
#     exit
#fi 

sleep 3

clear

timeout = 60

diskutil list

sleep 3

cal

du

ls
ls -l


sleep 3

whoami

sleep 3

clear

echo " "
echo " "

echo -e "   ⬅️  😊  ➡️        做一个简单的乘法计算! \a \n"

echo -e "\n"

sleep 1

read -p "请输入乘数A: " A     
read -p "请输入乘数B: " B     
echo -e "\n乘积为: "
echo -e "${A}*${B}" | bc

echo " "

echo " "

sleep 3

clear

/Users/saseny/Desktop/Script\ from\ Saseny/vim\ cal_pi.sh

sleep 3

clear

/Users/saseny/Desktop/Script\ from\ Saseny/vim\ file_perm.sh

sleep 3

clear

ifconfig

dig

sleep 3

clear

host -a

sleep 3

clear

top

sleep 20

clear


