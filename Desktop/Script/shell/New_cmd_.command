#!/bin/sh

#  new_cmd.sh
#  report
#
#  Created by Saseny on 2017/12/2.
#  Copyright © 2017年 Saseny. All rights reserved.

Dir=`dirname $0`
cp -rf $Dir/remove_burnin.command /tmp
error=$Dir/ERROR.xlsx

$Dir/BurninTools -b -l --error_code=$error

/tmp/remove_burnin.command

