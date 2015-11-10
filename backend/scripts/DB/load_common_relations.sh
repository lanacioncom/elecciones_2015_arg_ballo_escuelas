#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
CSV_PATH=$SCRIPTPATH'/../../data/comun'
CSV_FILE='relaciones_refine.csv'
# read configuration from env vars or default values
DATABASE_NAME=$1
TABLE_NAME='relaciones'
echo "loading data into $TABLE_NAME in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "TRUNCATE $TABLE_NAME; COPY $TABLE_NAME FROM '$CSV_PATH/$CSV_FILE' \
                           with delimiter as ',' CSV HEADER"