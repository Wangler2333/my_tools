#!/bin/bash

testfunc()
{
echo "$# parameters"
echo "$*"
echo  $*
echo "$@"
echo  $@
}
testfunc
testfunc a b c
testfunc a "b c"
testfunc a b c d e f g h i j k l m n o p q r s t u v w x y z
