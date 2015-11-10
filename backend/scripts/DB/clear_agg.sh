#!/bin/sh
SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
# read configuration from env vars or default values
DATABASE_NAME=$1
echo "drop aggregated tables in $DATABASE_NAME DB"
psql $DATABASE_NAME -q -c "
DROP TABLE IF EXISTS establecimientos_tmp;
DROP TABLE IF EXISTS localizaciones;
DROP TABLE IF EXISTS localizaciones_telegramas;
DROP TABLE IF EXISTS paso_resultados_establecimientos;
DROP TABLE IF EXISTS paso_totales_establecimientos;
DROP TABLE IF EXISTS paso_winner_establecimientos;
DROP TABLE IF EXISTS paso_resultados_localizaciones;
DROP TABLE IF EXISTS paso_totales_localizaciones;
DROP TABLE IF EXISTS paso_winner_localizaciones;
DROP TABLE IF EXISTS pv_resultados_establecimientos;
DROP TABLE IF EXISTS pv_totales_establecimientos;
DROP TABLE IF EXISTS pv_winner_establecimientos;
DROP TABLE IF EXISTS pv_resultados_localizaciones;
DROP TABLE IF EXISTS pv_totales_localizaciones;
DROP TABLE IF EXISTS pv_winner_localizaciones;
DROP TABLE IF EXISTS ballo_resultados_establecimientos;
DROP TABLE IF EXISTS ballo_totales_establecimientos;
DROP TABLE IF EXISTS ballo_winner_establecimientos;
DROP TABLE IF EXISTS ballo_diff_establecimientos;
DROP TABLE IF EXISTS ballo_resultados_localizaciones;
DROP TABLE IF EXISTS ballo_totales_localizaciones;
DROP TABLE IF EXISTS ballo_diff_localizaciones;
DROP TABLE IF EXISTS ballo_winner_localizaciones;
DROP TABLE IF EXISTS establecimientos_totales;
DROP TABLE IF EXISTS localizaciones_totales;
"