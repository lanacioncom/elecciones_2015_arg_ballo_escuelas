# coding: utf-8

clear_agg_sql = '''
DROP TABLE IF EXISTS establecimientos_tmp;
DROP TABLE IF EXISTS localizaciones;
DROP TABLE IF EXISTS localizaciones_telegramas;
DROP TABLE IF EXISTS paso_resultados_establecimientos;
DROP TABLE IF EXISTS paso_totales_establecimientos;
DROP TABLE IF EXISTS paso_resultados_localizaciones;
DROP TABLE IF EXISTS paso_totales_localizaciones;
DROP TABLE IF EXISTS cache_paso_winner_establecimientos;
DROP TABLE IF EXISTS cache_paso_winner_localizaciones;
DROP TABLE IF EXISTS pv_resultados_establecimientos;
DROP TABLE IF EXISTS pv_totales_establecimientos;
DROP TABLE IF EXISTS pv_resultados_localizaciones;
DROP TABLE IF EXISTS pv_totales_localizaciones;
DROP TABLE IF EXISTS cache_pv_winner_establecimientos;
DROP TABLE IF EXISTS cache_pv_winner_localizaciones;
DROP TABLE IF EXISTS cache_pv_resultados_establecimientos;
DROP TABLE IF EXISTS cache_pv_resultados_localizaciones;
DROP TABLE IF EXISTS ballo_resultados_establecimientos;
DROP TABLE IF EXISTS ballo_totales_establecimientos;
DROP TABLE IF EXISTS ballo_resultados_localizaciones;
DROP TABLE IF EXISTS ballo_totales_localizaciones;
DROP TABLE IF EXISTS cache_ballo_winner_establecimientos;
DROP TABLE IF EXISTS cache_ballo_winner_localizaciones;
DROP TABLE IF EXISTS cache_ballo_resultados_establecimientos;
DROP TABLE IF EXISTS cache_ballo_resultados_localizaciones;
DROP TABLE IF EXISTS cache_establecimientos_totales;
DROP TABLE IF EXISTS cache_localizaciones_totales;
'''

clear_hex_sql = '''
TRUNCATE hexagonos;
ALTER SEQUENCE hexagonos_id_hexagono_seq RESTART WITH 1;
'''


update_hex_seq = '''
SELECT setval('hexagonos_id_hexagono_seq', max(id_hexagono)) FROM hexagonos;
'''

clear_results_hex_sql = '''
TRUNCATE ballo_resultados_hexagonos;
TRUNCATE pv_resultados_hexagonos;
TRUNCATE paso_resultados_hexagonos;
TRUNCATE cache_paso_resultados_hexagonos;
TRUNCATE cache_ballo_resultados_hexagonos;
TRUNCATE cache_pv_resultados_hexagonos;
TRUNCATE cache_paso_winner_hexagonos;
TRUNCATE cache_ballo_winner_hexagonos;
TRUNCATE cache_pv_winner_hexagonos;
'''

clear_totals_hex_sql = '''
TRUNCATE cache_hexagonos_totales;
'''

clear_preprocessed_sql = '''
TRUNCATE establecimientos_mesas;
TRUNCATE ballo_totales_mesas;
TRUNCATE pv_totales_mesas;
TRUNCATE paso_totales_mesas;
TRUNCATE ballo_resultados_mesas;
ALTER SEQUENCE ballo_resultados_mesas_id_seq RESTART WITH 1;
TRUNCATE pv_resultados_mesas;
ALTER SEQUENCE pv_resultados_mesas_id_seq RESTART WITH 1;
TRUNCATE paso_resultados_mesas;
ALTER SEQUENCE paso_resultados_mesas_id_seq RESTART WITH 1;
'''
