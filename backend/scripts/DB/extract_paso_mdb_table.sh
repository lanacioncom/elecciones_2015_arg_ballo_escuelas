#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
DB_DATA_PATH=$SCRIPTPATH'/../../data/DB/paso'
DATABASE_NAME=PR_ARGENTINA2015.mdb
OUTPUT_PATH=$SCRIPTPATH'/../../data/paso' 
if [ $# -ne 1 ] 
then
    echo "Error: the script requires a tablename as input"
    exit 1    
fi
tablename=$1
mdb-export -D "%Y-%m-%d %H:%M:%S" $DB_DATA_PATH/$DATABASE_NAME $1 > $OUTPUT_PATH/$1.csv;