#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
OUTPUT_PATH=$SCRIPTPATH'/../../data/DB/output'
TIMESTAMP=$(/bin/date +"%Y%m%d_%H%M")
# read configuration from env vars or default values
DATABASE_NAME=$1
echo "dump $DATABASE_NAME in $OUTPUT_PATH with timestamp"
pg_dump -O $DATABASE_NAME | bzip2 > $OUTPUT_PATH/$DATABASE_NAME.$TIMESTAMP.sql.bz2