#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
SQL_PATH=$SCRIPTPATH'/../../data/sql'
# read configuration from env vars or default values
DATABASE_NAME=$1
echo "Creating $DATABASE_NAME schema"
psql -q -d $DATABASE_NAME -f $SQL_PATH/create_schema.sql