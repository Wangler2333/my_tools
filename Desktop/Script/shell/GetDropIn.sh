#!/bin/sh

#  BundleGetDropIn.sh
#  CleanRoomSelection
#
#  Created by Yaping Zhang on 4/19/13.
#  Copyright (c) 2013 Yaping Zhang. All rights reserved.
#!/bin/sh

################SERVER & LOG LIST FILE ######################
Server=172.24.9.123
username=skynet
PWD=skynet
ServerDropin=/Volumes/Data/NetDrop
LocalDropin=/NetDrop/DropIn
path=$(cd "$(dirname "$0")";pwd)

############SSH AUTO LOGIN##############################
Auto_Smart_ssh () {
expect -c "set timeout -1;
spawn ssh -o StrictHostKeyChecking=no $2 ${@:3};
expect {
*assword:* {send -- $1\r;
expect {
*denied* {exit 2;}
eof
}
}
eof {exit 1;}
}
"
return $?
}

#####CopyScriptToRemoteUnit#####
ping -t 5 $Server
IPCheck=$?
if [ $IPCheck -eq 0 ];then
mkdir -p $LocalDropin


sleep 1

auto_scp () {
            expect -c "set timeout -1;
            spawn scp -o StrictHostKeyChecking=no $1 ${@:2};
               expect {
                      *assword:* {send -- $PWD\r;
               expect {
                      *denied* {exit 1;}
                      eof
                    }
                }
             eof         {exit 1;}
             }
            "
           return $?
          }

auto_scp  $username@$Server:$ServerDropin/DropIn.pkg $LocalDropin/DropIn.pkg

fi
exit
