#!/bin/sh

wifi_msg="sid=\"BSTL\",msg-type=\"TEXT-XDBG\",TEXT=\"wl driver adapter not found\""

results=`grep "$wifi_msg" /Phoenix/Logs/processlog.plog | wc -l | sed 's/^[ \t]*//;s/[ \t]*$//'`
if [ $results -ne 0 ]; then
	echo "wifi not found"
exit 1
else
	echo "wifi found"
fi

exit 0