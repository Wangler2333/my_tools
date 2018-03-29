#!/bin/sh
cd "$(dirname "$0")"

astrisctl relay hippochannels 1
astrisctl relay dbgfifo 0
astrisctl relay dbgfifo 1

osascript -e 'tell application "Terminal"

	tell application "System Events" to tell process "Terminal" to keystroke "n" using command down
	delay 1
	tell application "Terminal" to do script "nanohippo -y -c 1250000,N,8,1 -d /dev/`ls /dev | grep -e cu.chimp-`" in selected tab of the front window

	delay 1

	tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
	delay 1
	tell application "Terminal" to do script "nanocom -y -P /usr/local/lib/nanocom/libnanocom_udp.dylib -d udp://127.0.0.1:31337" in selected tab of the front window

	delay 1
	tell application "Terminal" to activate
	tell application "System Events" to keystroke "\n"
	
	tell application "System Events" to tell process "Terminal" to keystroke "t" using command down
	delay 1
	tell application "Terminal" to do script  "nanocom -y -P /usr/local/lib/nanocom/libnanocom_udp.dylib -d udp://127.0.0.1:31339" in selected tab of the front window

	delay 1
	tell application "Terminal" to activate
	tell application "System Events" to keystroke "\n"
	
end tell'
