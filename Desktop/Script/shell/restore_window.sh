#!/bin/sh
# Hide the Phoenix UI window then show it again forcing it to redraw
/usr/bin/osascript -e 'tell application "Finder" to set visible of process "PhoenixCE" to false'
/usr/bin/osascript -e 'tell application "Finder" to set visible of process "PhoenixCE" to true'
