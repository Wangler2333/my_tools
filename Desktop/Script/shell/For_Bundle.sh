#!/bin/sh
# For bundle Create the last setup
# Created by Saseny on 2017/03/15
# The nvram setup check. 

Dir=`dirname $0`

#**********************************************************
FB_driver_Setup()
{
   sudo darwinup install  /AppleInternal/AppleIntelFramebuffer/AppleIntelKBLGraphicsFramebufferDiags.pax
   
   touch $Dir/FB_driver_Setup  # Touch message
   
   sleep 5
   sudo reboot 
}

#**********************************************************
AmbientLightSensorOSXService_rm()
{
   rm -rf /System/Library/Extensions/AmbientLightSensorOSXService.kext
   rm -Rf /System/Library/Caches/*.*
   sync
   sync
   sync
   touch /System/Library/Extensions 
   
   touch $Dir/AmbientLightSensorOSXService_rm  # Touch message
   
   sleep 5
   reboot
}

#**********************************************************
Before_DP()
{
   mv /usr/libexec/displaypolicyd /usr/libexec/displaypolicyd-released
   cp /AppleInternal/AppleGraphicsControl/displaypolicyd-factory /usr/libexec/displaypolicyd
   
   touch $Dir/Before_DP  # Touch message
   
   sleep 5
   reboot
}   

#**********************************************************
Debug_WiFi()
{
   sudo mv /System/Library/Extensions/IO80211Family.kext/Contents/PlugIns/AirPortBrcm4360.kext /System/Library/Extensions/IO80211Family.kext/Contents/PlugIns/AirPortBrcm4360.kext.hide
   sudo touch /System/Library/Extensions/
   
   touch $Dir/Debug_WiFi  # Touch message
   
   sleep 5
   reboot
}   

#*********************************** Check ****************
Check_WiFi_Debug()
{
   States=`/usr/local/bin/apple80211 -dri | grep -c "DEBUG MFG"`
   if [ $States -eq 0 ];then
      echo "[FAIL]: WiFi Debug not succeeded!"
      Debug_WiFi
   else
      echo "[PASS]: WiFi Debug is OK!"
   fi
}  

Check_AmbientLightSensorOSXService_rm()
{
   test -r /System/Library/Extensions/AmbientLightSensorOSXService.kext ; G=$?
   ls /System/Library/Caches/*.* &>/dev/null
   if [ $? -eq 0 ] && [ $G -eq 0 ];then
      echo "[FAIL]: AmbientLightSensorOSXService_rm not succeeded!"
      AmbientLightSensorOSXService_rm
   else
      echo "[PASS]: AmbientLightSensorOSXService_rm is OK!" 
   fi        
}

Check_Before_DP()
{
   test -r /usr/libexec/displaypolicyd-released
   if [ $? -ne 0 ];then
      echo "[FAIL]: Before_DP set not succeeded!"
      Before_DP
   else
      echo "[PASS]: Before_DP set is OK!"    
   fi   
}
     
Check_FB_Driver()
{
   test -r /System/Library/Extensions/AppleIntelKBLGraphicsFramebuffer.kext ; E=$?
   test -r /System/Library/Extensions/AppleIntelKBLGraphicsVAME.bundle ; F=$?
   if [ $E -ne 0 ] || [ $F -ne 0 ];then
      echo "[FAIL]: FB_Driver set not succeeded!" 
      FB_driver_Setup
   else
      echo "[PASS]: FB_Driver set is OK!"   
   fi             
}

Display_result()
{      
    sleep 1
    rm -rf $Dir/Debug_WiFi &>/dev/null
    rm -rf $Dir/FB_driver_Setup &>/dev/null
    rm -rf $Dir/AmbientLightSensorOSXService_rm &>/dev/null
    rm -rf $Dir/Before_DP &>/dev/null
    echo "-------------" ; echo "  [PASSED]  " ; echo "-------------" 
}

#**********************************************************
Check_States()
{
   test -r $Dir/Debug_WiFi ; A=$?
   test -r $Dir/FB_driver_Setup ; B=$?
   test -r $Dir/AmbientLightSensorOSXService_rm ; C=$?
   test -r $Dir/Before_DP ; D=$?
   
   if [ $A -ne 0 ];then
      Debug_WiFi
   elif [ $B -ne 0 ];then
      Check_WiFi_Debug
      FB_driver_Setup    
   elif [ $C -ne 0 ];then
      Check_WiFi_Debug
      Check_FB_Driver
      AmbientLightSensorOSXService_rm      
   elif [ $D -ne 0 ];then 
      Check_WiFi_Debug
      Check_FB_Driver
      Check_AmbientLightSensorOSXService_rm
      Before_DP   
   else     
      Check_WiFi_Debug
      Check_FB_Driver
      Check_AmbientLightSensorOSXService_rm
      Check_Before_DP 
      Display_result 
   fi
}      
   
#**************************** Main Script *****************

Check_WiFi_Debug
Check_FB_Driver
Check_AmbientLightSensorOSXService_rm
Check_Before_DP 
Display_result 
#Check_States