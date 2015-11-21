# coding: utf-8
from __future__ import with_statement
from fabric.api import *
from localdb import clear_agg, create_ix
import os

# Restrict visible functions
__all__ = ['run']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts')


@task
@runs_once
def run():
    '''process the DB initial data to extract polling station data'''
    with lcd(cwd):
        execute(clear_agg)
        local('python %s/process_results.py' % (scripts_path))
        execute(create_ix)
