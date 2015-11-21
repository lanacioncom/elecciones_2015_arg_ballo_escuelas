# coding: utf-8
from fabric.api import *
import localdb
import preprocess
import process
import hexagons
import cartodb
import export


@task
@runs_once
def run():
    '''runs the complete process'''
    execute(localdb.init)
    execute(preprocess.run)
    execute(process.run)
    execute(hexagons.run)
    execute(export.csv)


# DEFAULT TASK
@task(default=True)
def list_tasks():
    local('fab --list')
