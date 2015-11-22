# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB
from lqueries import clear_agg_sql
from lqueries import clear_hex_sql
from lqueries import clear_results_hex_sql
from lqueries import clear_totals_hex_sql
from lqueries import clear_preprocessed_sql
from lqueries import update_hex_seq

# Restrict visible functions
__all__ = ['init']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts/DB')
dbname = DB.split('/')[-1]

######################## HELPER FUNCTIONS ################################


def load(arr):
    '''load csvfiles into postgres table
    it expects an array of tuples in the following format
    ('table_name', 'path', 'csv_fname') or
    ('table_name', 'path') assumes the csv_fname is the same as the table name
        path: relative to the data folder
    '''
    cmd = '%(path)s/load_pg_table.sh %(db)s %(table)s %(csv_path)s'
    with lcd(cwd):
        for t in arr:
            abs_path = os.path.join(cwd, '../data', t[1])
            fpath = os.path.relpath(abs_path, scripts_path)
            # If the file name is not the same as the table
            if len(t) == 3:
                csvfile = '%s/%s.csv' % (fpath, t[2])
            else:
                csvfile = '%s/%s.csv' % (fpath, t[0])
            local(cmd %
                  {'path': scripts_path,
                   'db': dbname,
                   'table': t[0],
                   'csv_path': csvfile})


def load_wcols(arr):
    '''load csvfiles into postgres table
    it expects an array of tuples in the following format
    ('table_name', 'cols', 'path', 'csv_fname') or
    ('path', 'table_name' ' cols') assumes the csv_fname is the same as table
        path: relative to the data folder
    '''
    cmd = '%(path)s/load_pg_tcols.sh %(db)s %(table)s %(cols)s %(csv_path)s'
    with lcd(cwd):
        for t in arr:
            abs_path = os.path.join(cwd, '../data', t[2])
            fpath = os.path.relpath(abs_path, scripts_path)
            # If the file name is not the same as the table
            if len(t) == 4:
                csvfile = '%s/%s.csv' % (fpath, t[3])
            else:
                csvfile = '%s/%s.csv' % (fpath, t[0])
            local(cmd %
                  {'path': scripts_path,
                   'db': dbname,
                   'table': t[0],
                   'cols': t[1],
                   'csv_path': csvfile})


def exec_sqlfile(sqlfile):
    '''execute sqlfile into local postgres DB'''
    with lcd(cwd):
        local('%s/exec_pg_sqlfile.sh %s %s' % (scripts_path, dbname, sqlfile))


############################# TASKS ####################################

@task
@runs_once
def init():
    '''creates and loads initial data in the DB'''
    execute(recreate)
    execute(load_initial)
    execute(update_hexagons_seq)


@task
@runs_once
def recreate():
    '''drops, creates DB and required schema'''
    sqlfiles = ['create_extensions',
                'create_schema',
                'create_schema_hex',
                'create_cartodb_functions']
    # Create DB
    with lcd(cwd):
        local('%s/create_db.sh %s' % (scripts_path, dbname))
    # Get the path to the sqlfiles
    abs_path = os.path.join(cwd, '../data/sql')
    # Get the relative path
    fpath = os.path.relpath(abs_path, scripts_path)
    # loop all the sql files
    for s in sqlfiles:
        sqlfile = '%s/%s.sql' % (fpath, s)
        exec_sqlfile(sqlfile)


@task
@runs_once
def load_initial():
    '''loads input data into the DB'''
    cols = 'id_distrito,distrito,id_seccion,seccion'
    t_wcols = [
        ('ambitos',
         cols,
         'comun',
         'ambitos_refine')
    ]
    tables = [
        ('partidos', 'comun'),
        ('establecimientos', 'comun'),
        ('relaciones', 'comun'),
        ('hexagonos', 'comun')
    ]
    # Load tables with serials (needs cols)
    load_wcols(t_wcols)
    # Load other tables
    load(tables)


@task
@runs_once
def load_preprocessed():
    '''loads input data on the DB'''
    cols = 'key_circ,key_wo_circ,id_distrito,id_seccion,id_circuito,id_mesa'
    cols += ',id_partido,votos'
    t_wcols = [
        ('paso_resultados_mesas',
         cols,
         'paso/output',
         'mesascandidaturapresidente_key'),
        ('pv_resultados_mesas',
         cols,
         'pv/output',
         'mesascandidaturapresidente_key'),
        ('ballo_resultados_mesas',
         cols,
         'ballo/output',
         'mesascandidaturapresidente_key')
    ]
    tables = [
        ('establecimientos_mesas', 'comun/output', 'establecimientos_mesas'),
        ('paso_totales_mesas', 'paso/output', 'mesaspresidente_key'),
        ('pv_totales_mesas', 'pv/output', 'mesaspresidente_key'),
        ('ballo_totales_mesas', 'ballo/output', 'mesaspresidente_key')
    ]
    # Load tables with serials (needs cols)
    load_wcols(t_wcols)
    # Load other tables
    load(tables)


@task
@runs_once
def reset_preprocessed():
    '''truncates and resets seq for preprocessed tables'''
    sql = clear_preprocessed_sql
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def clear_agg():
    '''drops, creates DB and required schema'''
    sql = clear_agg_sql
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def reset_hexagons():
    '''truncates and resets seq for hexagons'''
    sql = clear_hex_sql
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def update_hexagons_seq():
    '''updates the hexagon serial id after an external load'''
    sql = update_hex_seq
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def reset_results_hexagons():
    '''truncates and resets seq for hexagon results'''
    sql = clear_results_hex_sql
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def reset_totals_hexagons():
    '''truncates and resets seq for hexagon totals'''
    sql = clear_totals_hex_sql
    with lcd(cwd):
        with hide('running'):
            local('%s/exec_pg_sql.sh %s "%s"' % (scripts_path, dbname, sql))


@task
@runs_once
def create_ix():
    '''create indexes in local DB to increase performance in calculations'''
    sqlfiles = ['create_ix']

    abs_path = os.path.join(cwd, '../data/sql')
    # Get the relative path
    fpath = os.path.relpath(abs_path, scripts_path)
    # Get the file name with relative path
    for s in sqlfiles:
        sqlfile = '%s/%s.sql' % (fpath, s)
        exec_sqlfile(sqlfile)


@task
@runs_once
def pg_dump():
    '''creates a timestamped DB dump'''
    with lcd(cwd):
        local('%s/pg_dump.sh %s' % (scripts_path, dbname))
