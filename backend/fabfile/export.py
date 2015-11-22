# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB
from localdb import pg_dump

# Restrict visible functions
__all__ = ['csv', 'dump']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts/yaml')


@task
@runs_once
def csv():
    '''export csv files to upload to cartodb'''
    with lcd(cwd):
        local('datafreeze --db %s %s/cartodb.yaml' % (DB, scripts_path))
        local('datafreeze --db %s %s/redaccion.yaml' % (DB, scripts_path))
        local('datafreeze --db %s %s/cartodb_hex.yaml' % (DB, scripts_path))


@task
@runs_once
def dump():
    '''export csv files to upload to cartodb'''
    with lcd(cwd):
        execute(pg_dump)
