#!/bin/bash
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
# read configuration from env vars or default values
OGR_PATH=${GDAL_PATH:-'/usr/local/bin'}
DB=${VRT_DB_CONNECTION:-'dbname="dbname" host="localhost" port="5432"  user="user" password="pass"'}
VRT_PATH=$SCRIPTPATH'/../../data/comun'
VRT_FILE='establecimientos_geo.vrt'
# table name to create in postgis
TABLE_NAME='establecimientos_geo'
echo "****************************************"
echo "set GDAL_PATH env var or change default to point to the ogr2ogr binary"
echo "set VRT_DB_CONNECTION env var or change default to point to the target DB"
echo "****************************************"
echo "loading csv through $VRT_FILE into postgis"
$OGR_PATH/ogr2ogr -nlt PROMOTE_TO_MULTI -progress -nln $TABLE_NAME -preserve_fid -skipfailures -lco PRECISION=no -f PostgreSQL PG:"$DB" $VRT_PATH/$VRT_FILE