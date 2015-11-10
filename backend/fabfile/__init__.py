# coding: utf-8
from fabric.api import *
import localdb
import preprocess
import process
import cartodb
import export


@task
@runs_once
def run():
    '''runs the complete process'''
    execute(init)
    execute(preprocess)
    execute(process)
    execute(export)


# DEFAULT TASK
@task(default=True)
def list_tasks():
    local('fab --list')
