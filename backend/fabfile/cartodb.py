# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from urllib import quote
from settings import CDB_USER, CDB_KEY
import cdbqueries

# Restrict visible functions
__all__ = ['import_common', 'import_shortcuts',
           'import_hexagons',
           'import_ballo_loc_results',
           'import_pv_loc_results',
           'import_paso_loc_results',
           'import_hex_winners',
           'search', 'crowdsource',
           'create_indexes']

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
def import_table(relpath, tablename):
    '''import a table to cartodb'''
    with lcd(cwd):
        execute(run_query, drop_sql(tablename))
        with hide('running'):
            local('%s/import_csv_cartodb.sh %s/%s/%s.csv %s %s'
                  % (scripts_path,
                     data_path,
                     relpath,
                     tablename,
                     CDB_USER,
                     CDB_KEY))


@task
@runs_once
def import_common():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'localizaciones', 'arg_ballo_partidos')
    execute(import_table, 'localizaciones', 'arg_ballo_localizaciones')
    execute(import_table, 'localizaciones', 'arg_ballo_rel_est_loc')


@task
@runs_once
def import_shortcuts():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'localizaciones', 'arg_ballo_loc_telegramas')


@task
@runs_once
def import_ballo_loc_results():
    '''import location csv files into cartodb using import && SQL APIs'''
    execute(import_table, 'localizaciones', 'cache_arg_ballo_loc_ganador')
    execute(import_table, 'localizaciones', 'cache_arg_ballo_loc_votos')
    execute(import_table, 'hexagonos', 'cache_arg_ballo_hex_votos')


@task
@runs_once
def import_pv_loc_results():
    '''import location csv files into cartodb using import && SQL APIs'''
    execute(import_table, 'localizaciones', 'cache_arg_pv_loc_ganador')
    execute(import_table, 'localizaciones', 'cache_arg_pv_loc_votos')
    execute(import_table, 'hexagonos', 'cache_arg_pv_hex_votos')


@task
@runs_once
def import_paso_loc_results():
    '''import location csv files into cartodb using import && SQL APIs'''
    execute(import_table, 'localizaciones', 'cache_arg_paso_loc_ganador')
    execute(import_table, 'localizaciones', 'cache_arg_paso_loc_votos')
    execute(import_table, 'hexagonos', 'cache_arg_paso_hex_votos')


@task
@runs_once
def import_hex_winners():
    '''import hex winners for each election'''
    execute(import_table, 'hexagonos', 'cache_arg_ballo_hex_ganador')
    execute(import_table, 'hexagonos', 'cache_arg_pv_hex_ganador')
    execute(import_table, 'hexagonos', 'cache_arg_paso_hex_ganador')


@task
@runs_once
def import_hexagons():
    '''import cached haxagon csv files into cartodb using import && SQL APIs'''
    execute(import_table, 'hexagonos', 'arg_ballo_hexagonos')


@task
@runs_once
def import_est_results():
    '''import csv files into cartodb using import API'''
    execute(import_table, 'establecimientos', 'arg_ballo_establecimientos')
    execute(import_table, 'establecimientos', 'cache_arg_ballo_est_ganador')
    execute(import_table, 'establecimientos', 'cache_arg_ballo_est_votos')


@task
@runs_once
def create_indexes():
    '''create indexes for ballotage cartodb tables'''
    with lcd(cwd):
        execute(run_query, cdbqueries.location_index_sql)
        execute(run_query, cdbqueries.loc_index_name_sql)
        execute(run_query, cdbqueries.loc_index_address_sql)
        execute(run_query, cdbqueries.loc_index_city_sql)
        execute(run_query, cdbqueries.telegrams_index_sql)
        execute(run_query, cdbqueries.diff_index_loc_sql)
        execute(run_query, cdbqueries.diff_index_party_sql)
        execute(run_query, cdbqueries.ballo_hexagonos_index_sql)
        execute(run_query, cdbqueries.cache_ballo_hex_res_index_hex_sql)
        execute(run_query, cdbqueries.cache_ballo_hex_res_index_party_sql)
        execute(run_query, cdbqueries.cache_pv_hex_res_index_hex_sql)
        execute(run_query, cdbqueries.cache_pv_hex_res_index_party_sql)
        execute(run_query, cdbqueries.paso_hex_res_index_hex_sql)
        execute(run_query, cdbqueries.paso_hex_res_index_party_sql)


@task
@runs_once
def search():
    '''cartodb winner table setting full text search'''

    with lcd(cwd):
        execute(run_query, cdbqueries.search_alter_sql)
        execute(run_query, cdbqueries.search_index_sql)
        execute(run_query, cdbqueries.search_update_sql)


@task
@runs_once
def crowdsource():
    '''cartodb crowdsource functionality'''

    with lcd(cwd):
        execute(run_query, drop_sql('arg_ballo_crowdsource'))
        execute(run_query, cdbqueries.crowd_create_sql)
        execute(run_query, cdbqueries.crowd_index_sql)
        execute(run_query, cdbqueries.crowd_editor_sql)
        execute(run_query, cdbqueries.crowd_function_sql)

