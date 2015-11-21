#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
if [ $# -eq 2 ]
  then
    DATABASE_NAME=$1
    SQL=$2
else
    echo "Error: this script needs 2 params: DB, SQL_QUERIES"
    exit 1
fi
echo "drop aggregated tables in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "$SQL"
