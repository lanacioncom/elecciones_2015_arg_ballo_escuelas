# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB
from localdb import reset_hexagons
from localdb import reset_results_hexagons
from localdb import reset_totals_hexagons

# Restrict visible functions
__all__ = ['create', 'create_all', 'create_antartida', 'run',
           'calc_results', 'calc_cache_results',
           'calc_results_all', 'calc_totals',
           'reset', 'reset_results', 'reset_totals']

# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts')


@task
@runs_once
def reset():
    '''reset the hexagon table'''
    with lcd(cwd):
        execute(reset_hexagons)


@task
@runs_once
def reset_results():
    '''reset the calculated hexagon results'''
    with lcd(cwd):
        execute(reset_results_hexagons)


@task
@runs_once
def reset_totals():
    '''reset the calculated hexagon results'''
    with lcd(cwd):
        execute(reset_totals_hexagons)


@task
@runs_once
def calc_results(elec=2):
    '''calculates aggregated results for each hexagon and election'''
    with lcd(cwd):
        local('python %s/process_results_hexagons.py -e %s'
              % (scripts_path, elec))


@task
@runs_once
def calc_cache_results(elec=2):
    '''calculates aggregated results for each hexagon and election'''
    with lcd(cwd):
        local('python %s/process_results_hexagons.py -e %s -c'
              % (scripts_path, elec))


@task
@runs_once
def calc_winner_results(elec=2):
    '''calculates winner results for each hexagon and election'''
    with lcd(cwd):
        local('python %s/process_results_hexagons.py -e %s -w'
              % (scripts_path, elec))


@task
@runs_once
def calc_results_all():
    '''calculates all aggregated results for each hexagon'''
    with lcd(cwd):
        execute(reset_results)
        for i in range(0, 3):
            local('python %s/process_results_hexagons.py -e %s'
                  % (scripts_path, i))
        for i in range(0, 3):
            local('python %s/process_results_hexagons.py -e %s -c'
                  % (scripts_path, i))
        for i in range(0, 3):
            local('python %s/process_results_hexagons.py -e %s -w'
                  % (scripts_path, i))


@task
@runs_once
def calc_totals():
    '''calculates all aggregated results for each hexagon'''
    with lcd(cwd):
        execute(reset_totals)
        for i in range(0, 3):
            local('python %s/process_totals_hexagons.py -e %s'
                  % (scripts_path, i))
        local('python %s/process_totals_hexagons.py -c' % (scripts_path))


@task
@runs_once
def run():
    '''calculates totals and results for hexagons'''
    execute(calc_totals)
    execute(calc_results_all)
    for i in range(0, 3):
            local('python %s/update_cache_status.py -e %s -x' % (scripts_path,
                                                                 i))


@task
@runs_once
def create(zoom=4, size=3, antar=False, low=False):
    '''creates a grid for a particular zoom level and size multiplier'''
    with lcd(cwd):
        local('python %s/create_hexagons.py -z %s -s %s'
              % (scripts_path, zoom, size))


@task
@runs_once
def create_antartida(zoom=4, size=3):
    '''creates antartida hex for a particular zoom level and size multiplier'''
    with lcd(cwd):
        local('python %s/create_hexagons.py -z %s -s %s -a'
              % (scripts_path, zoom, size))


@task
@runs_once
def create_all():
    '''creates hexagons for levels 4 through 12'''
    with lcd(cwd):
        execute(reset)
        for i in range(4, 13):
            local('python %s/create_hexagons.py -z %s -s %s'
                  % (scripts_path, i, 3))
            local('python %s/create_hexagons.py -z %s -s %s -a'
                  % (scripts_path, i, 3))
        for i in range(13, 15):
            local('python %s/create_hexagons.py -z %s -s %s -l'
                  % (scripts_path, i, 3))
