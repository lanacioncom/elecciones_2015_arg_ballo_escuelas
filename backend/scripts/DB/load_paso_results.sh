#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
CSV_PATH=$SCRIPTPATH'/../../data/paso/output'
CSV_FILE='mesascandidaturapresidente_key.csv'
# read configuration from env vars or default values
DATABASE_NAME=$1
TABLE_NAME=paso_resultados_mesas
COLUMNS=key_circ,key_wo_circ,id_distrito,id_seccion,id_circuito,id_mesa,id_partido,votos
echo "loading data into $TABLE_NAME in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "TRUNCATE $TABLE_NAME; COPY $TABLE_NAME($COLUMNS) FROM '$CSV_PATH/$CSV_FILE' \
                           with delimiter as ',' CSV HEADER"