
return=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`

while [ $return -eq 0 ]
do
echo "Network Cable not connected"
sleep 1
return=`system_profiler SPUSBDataType | grep -c "Apple USB Ethernet Adapter"`
done

sleep 1
/usr/sbin/networksetup -setmanual "Apple USB Ethernet Adapter" 192.168.100.5 255.255.255.0


while [ ! -f /Phoenix/Logs/WiPAS_SFS/AntVendor.txt ]
do

echo "Getting SFS int Vendor file"
sleep 1

done
