#!/bin/sh

DSPPlugin="/AppleInternal/Diagnostics/OS/Plugins/Display.plugin"
#CAMPlugin="/AppleInternal/Diagnostics/OS/Plugins/Camera.plugin"

if [ ! -d "${DSPPlugin}" ]; then
 echo "Missing Display plugin"
 else
 echo "OK"
fi
