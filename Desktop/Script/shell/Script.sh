#!/bin/sh

#  Script.sh
#  123
#
#  Created by Saseny on 9/29/16.
#  Copyright © 2016 Saseny. All rights reserved.

set -x

AB()
{
echo " Have CM Bundle , and CM Bundel is : $CM . "
echo " Copy CMimageList.plist "
cp -rf /Volumes/Download/private/var/root/Desktop/081/CMImageList.plist /Phoenix/Tools/Settings
echo " Copy CMBundleCheck.sh "
cp -rf /Volumes/Download/private/var/root/Desktop/081/CmBundleCheck.sh /TE_Support/Scripts/Test_Process
echo " Copy x3 PI Table "
rm -rf /Phoenix/Tables
cp -rf /Volumes/Download/private/var/root/Desktop/M8/Tables /Phoenix
}
ABC()
{
echo " There haven't CM Bundle , Need Copy CM Bundle . "
echo " Copy CM Bundle "
cp -rf /Volumes/Download/694-05404-081.dmg /private/var/root/Desktop
echo " Copy CMimageList.plist "
cp -rf /Volumes/Download/private/var/root/Desktop/081/CMImageList.plist /Phoenix/Tools/Settings
echo " Copy CMBundleCheck.sh "
cp -rf /Volumes/Download/private/var/root/Desktop/081/CmBundleCheck.sh /TE_Support/Scripts/Test_Process
echo " Copy x3 PI Table "
rm -rf /Phoenix/Tables
cp -rf /Volumes/Download/private/var/root/Desktop/M8/Tables /Phoenix
}




CM=`ls /*.dmg | grep 694 | awk -F '-' '{print$3}' | awk -F '.' '{print$1}'`
A="081"

if [ -n $CM ]
  then
    if [ $CM = $A ]
      then
        echo " Have CM Bundle , and CM Bundel is : $CM . "
        AB
      else
        echo " Have CM Bundle , and CM Bundel is : $CM . Not 081 , need Copy "
        ABC
    fi
  else
   ABC
fi
/TE_Support/Tools/Phoenix/cleanup_Phoenix2.command
sleep 3
reboot
