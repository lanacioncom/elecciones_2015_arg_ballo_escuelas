# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB
from localdb import pg_dump

# Restrict visible functions
__all__ = ['run', 'csv_cartodb', 'csv_newsroom', 'dump']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts/yaml')


@task
@runs_once
def csv_cartodb():
    '''export csv files to upload to cartodb'''
    with lcd(cwd):
        local('datafreeze --db %s %s/cartodb.yaml' % (DB, scripts_path))
        local('datafreeze --db %s %s/cartodb_hex.yaml' % (DB, scripts_path))


@task
@runs_once
def csv_newsroom():
    '''export csv files for a more analytic approach'''
    with lcd(cwd):
        local('datafreeze --db %s %s/redaccion.yaml' % (DB, scripts_path))


@task
@runs_once
def run():
    '''export all the csv files at once'''
    execute(csv_cartodb)
    execute(csv_newsroom)


@task
@runs_once
def dump():
    '''export csv files to upload to cartodb'''
    with lcd(cwd):
        execute(pg_dump)
