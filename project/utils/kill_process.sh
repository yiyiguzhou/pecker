#!/bin/bash
# echo `ps -ef | grep python`
if [ $# -lt 1 ]
then
  echo "缺少参数：procedure_name"
  exit 0
fi

ID=`ps -ef | grep $1 | grep -v "$0" | grep -v "grep" | awk '{print $2}'`
echo $ID

for id in $ID 
do
  kill -9 $id
  echo "killed $id"
done
