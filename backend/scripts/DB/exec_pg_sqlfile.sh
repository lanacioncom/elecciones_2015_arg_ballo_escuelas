#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
if [ $# -eq 2 ]
  then
    DATABASE_NAME=$1
    SQLFILE=$SCRIPTPATH'/'$2
else
    echo "Error: this script needs 2 params: DB, SQLFILE"
    exit 1
fi
echo "execute $SQLFILE in $DATABASE_NAME DB"
psql -q -d $DATABASE_NAME -f $SQLFILE
