# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from urllib import quote
from settings import CDB_USER, CDB_KEY

# Restrict visible functions
__all__ = ['import_common', 'import_shortcuts', 'import_est_results',
           'import_loc_results', 'search', 'crowdsource']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts/cartodb')
data_path = os.path.join(cwd, '../data/cartodb')


def drop_sql(tablename):
    '''creates a DROP statement url escaped'''
    return 'DROP TABLE IF EXISTS %s;' % (tablename)


@task
def run_query(query):
    '''import a table to cartodb'''
    sql_url = quote(query, safe='/')

    with lcd(cwd):
        with hide('running'):
            local('%s/run_sql_cartodb.sh %s %s %s'
                  % (scripts_path,
                     sql_url,
                     CDB_USER,
                     CDB_KEY))


@task
def import_table(tablename):
    '''import a table to cartodb'''
    with lcd(cwd):
        execute(run_query, drop_sql(tablename))
        with hide('running'):
            local('%s/import_csv_cartodb.sh %s/%s.csv %s %s'
                  % (scripts_path,
                     data_path,
                     tablename,
                     CDB_USER,
                     CDB_KEY))


@task
@runs_once
def import_common():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'arg_ballo_partidos')
    execute(import_table, 'arg_ballo_establecimientos')
    execute(import_table, 'arg_ballo_localizaciones')


@task
@runs_once
def import_shortcuts():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'arg_ballo_loc_telegramas')
    execute(import_table, 'arg_ballo_rel_est_loc')


@task
@runs_once
def import_est_results():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'arg_ballo_est_ganador')
    execute(import_table, 'arg_ballo_est_diff_votos')


@task
@runs_once
def import_loc_results():
    '''import location csv files into cartodb using import && SQL APIs'''
    execute(import_table, 'arg_ballo_loc_ganador')
    execute(import_table, 'arg_ballo_loc_diff_votos')


@task
@runs_once
def search():
    '''cartodb winner table setting full text search'''

    alter_sql = '''
ALTER TABLE arg_ballo_loc_ganador
ADD COLUMN tsv tsvector;
'''
    create_index_sql = '''
CREATE INDEX arg_ballo_loc_ganador_tsv_idx 
ON arg_ballo_loc_ganador USING gin(tsv);
'''
    update_sql = '''
UPDATE arg_ballo_loc_ganador
SET tsv = setweight(to_tsvector('pg_catalog.spanish', coalesce(nombre,'')), 'A')
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(direccion,'')), 'B') 
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(localidad,'')), 'C') 
|| setweight(to_tsvector('pg_catalog.spanish', coalesce(seccion,'')), 'D');
'''

    with lcd(cwd):
        execute(run_query, alter_sql)
        execute(run_query, create_index_sql)
        execute(run_query, update_sql)


@task
@runs_once
def crowdsource():
    '''cartodb crowdsource functionality'''

    create_sql = '''
CREATE TABLE IF NOT EXISTS arg_ballo_crowdsource (
    id_agrupado integer,
    valido boolean,
    comentario character varying(200));
'''
    create_index_sql = '''
CREATE INDEX arg_ballo_crowdsource_poll_idx
ON arg_ballo_crowdsource USING btree (id_agrupado);;
'''
    show_editor_sql = '''
    select cdb_cartodbfytable('lndata','arg_ballo_crowdsource');
'''
    crowdsource_function_sql = '''
-- Returns the cartodb_id of the inserted row:
DROP FUNCTION IF EXISTS ballo_crowdsource_geo(integer, boolean, text);
CREATE OR REPLACE FUNCTION ballo_crowdsource_geo(id_agrupado integer, valido boolean, comentario text)
RETURNS INTEGER
LANGUAGE plpgsql SECURITY DEFINER
RETURNS NULL ON NULL INPUT
AS $$
DECLARE
    id INTEGER;
BEGIN
    BEGIN
    INSERT INTO arg_ballo_crowdsource(id_agrupado,valido,comentario) VALUES (id_agrupado,valido,comentario) RETURNING cartodb_id into id;
        RETURN id;
    EXCEPTION WHEN OTHERS THEN /*Catch all*/
        RETURN 0;
    END;
END;
$$;
--set permissions to publicuser
GRANT EXECUTE ON FUNCTION ballo_crowdsource_geo(integer, boolean, text) TO publicuser;
'''
    with lcd(cwd):
        execute(run_query, drop_sql('arg_ballo_crowdsource'))
        execute(run_query, create_sql)
        execute(run_query, create_index_sql)
        execute(run_query, show_editor_sql)
        execute(run_query, crowdsource_function_sql)
