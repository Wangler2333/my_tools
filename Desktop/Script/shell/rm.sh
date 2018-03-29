#!/bin/rm
# 自删除脚本
# 当你运行这个脚本时，基本上什么都不会发生...当然这个文件消失不见了
WHATEVEN=65
echo "This line will never print!"
exit $WHATEVEN     # 不要紧，脚本是不会在这退出的
