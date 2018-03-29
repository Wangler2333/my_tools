#!/bin/bash
sel_v=1
declare -a voices=("Agnes" "Albert" "Alex" "Bad" "Bahh" "Bells" "Boing" "Bruce" "Bubbles" "Cellos" "Daniel" "Deranged" "Fred" "Good" "Junior" "Karen" "Kathy" "Moira" "Pipe" "Princess" "Ralph" "Samantha" "Tessa" "Trinoids" "Veena" "Vicki" "Victoria" "Whisper" "Zarvox")

mtreport set 0xF3 0x0A
mtreport set 0xC8 0x3E
echo "Monitor Started"
if syslog -w -B | grep -q "AppleHSSPI.*CRC"; then echo "CRC Error Detected!"; say "CRC Error Detected!"; echo "Log saving please wait..."; syslog | grep HSSPI > ~/Desktop/syslogCRC.txt; echo "syslogCRC.txt has been saved to desktop."; fi

if [ -t 0 ]; then stty -echo -icanon time 0 min 0; fi

while [ "x$keypress" = "x" ]; do
  let count+=1
  echo -ne $count'\r'
  sel_v=`jot -r 1  1 ${#voices[@]}`
  say -v ${voices[$sel_v]} "CRC Error Detected"
  read keypress
done

if [ -t 0 ]; then stty sane; fi

#echo "You pressed '$keypress' after $count loop iterations"
echo "Thanks for using this script. Please email syslogCRC.txt and context of your experiment to Kianoosh Salami <ksalami@apple.com> CC: Jordan Raetz <jraetz@apple.com>"
exit 0


