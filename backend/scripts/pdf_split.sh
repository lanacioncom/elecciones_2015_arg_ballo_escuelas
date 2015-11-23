#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
path=$SCRIPTPATH'/../data/telegrams'
echo "$path"
cd "$path/pdf" || { echo "directory does not exist"; exit 1;}
n=0
for i in *
do
  if [ $((n+=1)) -gt 5 ]; then
    n=1
  fi
  todir="../pdf$n"
  [ -d "$todir" ] || mkdir "$todir" 
  mv "$i" "$todir" 
done