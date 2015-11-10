# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from localdb import load_preprocessed

# Restrict visible functions
__all__ = ['run']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts')


@task
@runs_once
def run():
    '''execute preprocessing tasks on the input datasets'''
    execute(polling_stations)
    execute(totals)
    execute(results)
    execute(load_preprocessed)


@task
@runs_once
def polling_stations():
    with lcd(cwd):
        local('python %s/extract_polling_station_tables.py' % (scripts_path))


@task
@runs_once
def results():
    with lcd(cwd):
        local('python %s/generate_results_key.py' % (scripts_path))


@task
@runs_once
def totals():
    with lcd(cwd):
        local('python %s/generate_totals_key.py' % (scripts_path))