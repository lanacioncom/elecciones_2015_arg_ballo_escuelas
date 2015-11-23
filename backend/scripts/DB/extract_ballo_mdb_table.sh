#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
DB_DATA_PATH=$SCRIPTPATH'/../../data/DB/ballo'
DATABASE_NAME=B_ARGENTINA2015.mdb
OUTPUT_PATH=$SCRIPTPATH'/../../data/ballo' 
if [ $# -ne 1 ] 
then
    echo "Error: the script requires a tablename as input"
    exit 1
fi
tablename=$1
mdb-export -D "%Y-%m-%d %H:%M:%S" -q "'" $DB_DATA_PATH/$DATABASE_NAME $1 > $OUTPUT_PATH/$1.csv;