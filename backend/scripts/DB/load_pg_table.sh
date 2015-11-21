#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
if [ $# -eq 3 ]
  then
    DATABASE_NAME=$1
    TABLE_NAME=$2
    CSV_FILE=$SCRIPTPATH'/'$3
else
    echo "Error: this script needs 3 params: DB, TABLE, CSV_FILE_W_PATH"
    exit 1
fi
echo "loading data into $TABLE_NAME in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "TRUNCATE $TABLE_NAME; COPY $TABLE_NAME FROM '$CSV_FILE' \
                           with delimiter as ',' CSV HEADER"