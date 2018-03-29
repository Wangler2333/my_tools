#!/bin/sh
# HT LAW
# Check display brightness if is in auto mode, if yes then disable it.
#
# ====================================================================================


bezelService=/usr/local/bin/BezelServicesTest

return=`$bezelService -a dAuto`
statusReturn=`echo $return | sed 's/.*: //'`
echo $return
echo "***************************************************************************"
echo "Status (before):\t$statusReturn"

$bezelService -a dAuto=false

return=`$bezelService -a dAuto`
statusReturn=`echo $return | sed 's/.*: //'`
echo "***************************************************************************"
echo "Status (after):\t\t$statusReturn"