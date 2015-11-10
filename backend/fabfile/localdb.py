# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB

# Restrict visible functions
__all__ = ['init']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts/DB')
dbname = DB.split('/')[-1]


@task
@runs_once
def init():
    '''creates and loads initial data in the DB'''
    execute(recreate)
    execute(load)


@task
@runs_once
def recreate():
    '''drops, creates DB and required schema'''
    with lcd(cwd):
        local('%s/create_db.sh %s' % (scripts_path, dbname))
        local('%s/create_schema.sh %s' % (scripts_path, dbname))


@task
@runs_once
def load():
    '''loads input data into the DB'''
    with lcd(cwd):
        local('%s/load_common_parties.sh %s' % (scripts_path, dbname))
        local('%s/load_common_sections.sh %s' % (scripts_path, dbname))
        local('%s/load_common_polling_stations_geo.sh %s' % (scripts_path,
                                                             dbname))
        local('%s/load_common_relations.sh %s' % (scripts_path, dbname))


@task
@runs_once
def load_preprocessed():
    '''loads input data on the DB'''
    with lcd(cwd):
        local('%s/load_common_polling_tables.sh %s' % (scripts_path, dbname))
        local('%s/load_paso_totals.sh %s' % (scripts_path, dbname))
        local('%s/load_paso_results.sh %s' % (scripts_path, dbname))
        local('%s/load_pv_totals.sh %s' % (scripts_path, dbname))
        local('%s/load_pv_results.sh %s' % (scripts_path, dbname))
        local('%s/load_ballo_totals.sh %s' % (scripts_path, dbname))
        local('%s/load_ballo_results.sh %s' % (scripts_path, dbname))


@task
@runs_once
def clear_agg():
    '''drops, creates DB and required schema'''
    with lcd(cwd):
        local('%s/clear_agg.sh %s' % (scripts_path, dbname))


@task
@runs_once
def pg_dump():
    '''creates a timestamped DB dump'''
    with lcd(cwd):
        local('%s/pg_dump.sh %s' % (scripts_path, dbname))
