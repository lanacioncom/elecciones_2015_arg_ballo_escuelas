#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
if [ $# -eq 4 ]
  then
    DATABASE_NAME=$1
    TABLE_NAME=$2
    COLS=$3
    CSV_FILE=$SCRIPTPATH'/'$4
else
    echo "Error: this script needs 4 params: DB, TABLE, COLS, CSV_FILE_W_PATH"
    exit 1
fi
echo "loading data into $TABLE_NAME in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "TRUNCATE $TABLE_NAME; COPY $TABLE_NAME($COLS) FROM '$CSV_FILE' \
                           with delimiter as ',' CSV HEADER"