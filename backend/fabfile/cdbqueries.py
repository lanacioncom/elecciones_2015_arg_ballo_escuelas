# coding: utf-8

loc_index_id_sql = '''
CREATE INDEX arg_ballo_localizaciones_ix_agrupado
ON arg_ballo_localizaciones USING btree(id_agrupado);
'''

loc_search_index_name_sql = '''
CREATE INDEX arg_ballo_localizaciones_ix_nombre
ON arg_ballo_localizaciones USING btree(nombre);
'''

loc_search_index_address_sql = '''
CREATE INDEX arg_ballo_localizaciones_ix_direccion
ON arg_ballo_localizaciones USING btree(direccion);
'''

loc_search_index_city_sql = '''
CREATE INDEX arg_ballo_localizaciones_ix_localidad
ON arg_ballo_localizaciones USING btree(localidad);
'''

hex_index_id_sql = '''
CREATE INDEX arg_ballo_hexagonos_ix_hexagono
ON arg_ballo_hexagonos USING btree(id_hexagono);
'''

telegrams_index_id_sql = '''
CREATE INDEX arg_ballo_loc_telegramas_ix_agrupado
ON arg_ballo_loc_telegramas USING btree(id_agrupado);
'''

cache_ballo_loc_res_index_id_sql = '''
CREATE INDEX cache_arg_ballo_loc_votos_ix_agrupado
ON cache_arg_ballo_loc_votos USING btree(id_agrupado);
'''

cache_ballo_loc_res_index_party_sql = '''
CREATE INDEX cache_arg_ballo_loc_votos_ix_partido
ON cache_arg_ballo_loc_votos USING btree(id_partido);
'''

cache_ballo_hex_res_index_id_sql = '''
CREATE INDEX cache_arg_ballo_hex_votos_ix_hexagono
ON cache_arg_ballo_hex_votos USING btree(id_hexagono);
'''

cache_ballo_hex_res_index_party_sql = '''
CREATE INDEX cache_arg_ballo_hex_votos_ix_partido
ON cache_arg_ballo_hex_votos USING btree(id_partido);
'''

cache_pv_loc_res_index_id_sql = '''
CREATE INDEX cache_arg_pv_loc_votos_ix_agrupado
ON cache_arg_pv_loc_votos USING btree(id_agrupado);
'''

cache_pv_loc_res_index_party_sql = '''
CREATE INDEX cache_arg_pv_loc_votos_ix_partido
ON cache_arg_pv_loc_votos USING btree(id_partido);
'''

cache_pv_hex_res_index_id_sql = '''
CREATE INDEX cache_arg_pv_hex_votos_ix_hexagono
ON cache_arg_pv_hex_votos USING btree(id_hexagono);
'''

cache_pv_hex_res_index_party_sql = '''
CREATE INDEX cache_arg_pv_hex_votos_ix_partido
ON cache_arg_pv_hex_votos USING btree(id_partido);
'''

cache_paso_loc_res_index_id_sql = '''
CREATE INDEX cache_arg_paso_loc_votos_ix_agrupado
ON cache_arg_paso_loc_votos USING btree(id_agrupado);
'''

cache_paso_loc_res_index_party_sql = '''
CREATE INDEX cache_arg_paso_loc_votos_ix_partido
ON cache_arg_paso_loc_votos USING btree(id_partido);
'''

cache_paso_hex_res_index_id_sql = '''
CREATE INDEX cache_arg_paso_hex_votos_ix_hexagono
ON cache_arg_paso_hex_votos USING btree(id_hexagono);
'''

cache_paso_hex_res_index_party_sql = '''
CREATE INDEX cache_arg_paso_hex_votos_ix_partido
ON cache_arg_paso_hex_votos USING btree(id_partido);
'''

search_alter_sql = '''
ALTER TABLE arg_ballo_localizaciones
ADD COLUMN tsv tsvector;
'''
search_index_sql = '''
CREATE INDEX arg_ballo_localizaciones_tsv_idx
ON arg_ballo_localizaciones USING gin(tsv);
'''
search_update_sql = '''
UPDATE arg_ballo_localizaciones SET tsv =
setweight(to_tsvector('pg_catalog.spanish', coalesce(nombre,'')), 'A')
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(direccion,'')), 'B')
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(localidad,'')), 'C')
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(seccion,'')), 'D');
'''

crowd_create_sql = '''
CREATE TABLE IF NOT EXISTS arg_ballo_crowdsource (
    id_agrupado integer,
    valido boolean,
    comentario character varying(200));
'''
crowd_index_sql = '''
CREATE INDEX arg_ballo_crowdsource_poll_idx
ON arg_ballo_crowdsource USING btree (id_agrupado);;
'''

crowd_editor_sql = '''
    select cdb_cartodbfytable('lndata','arg_ballo_crowdsource');
'''

crowd_function_sql = '''
-- Returns the cartodb_id of the inserted row:
DROP FUNCTION IF EXISTS ballo_crowdsource_geo(integer, boolean, text);
CREATE OR REPLACE FUNCTION ballo_crowdsource_geo(id_agrupado integer,
                                                 valido boolean,
                                                 comentario text)
RETURNS INTEGER
LANGUAGE plpgsql SECURITY DEFINER
RETURNS NULL ON NULL INPUT
AS $$
DECLARE
    id INTEGER;
BEGIN
    BEGIN
    INSERT INTO arg_ballo_crowdsource(id_agrupado,valido,comentario) VALUES
    (id_agrupado,valido,comentario) RETURNING cartodb_id into id;
        RETURN id;
    EXCEPTION WHEN OTHERS THEN /*Catch all*/
        RETURN 0;
    END;
END;
$$;
--set permissions to publicuser
GRANT EXECUTE ON FUNCTION ballo_crowdsource_geo(integer, boolean, text)
TO publicuser;
'''
