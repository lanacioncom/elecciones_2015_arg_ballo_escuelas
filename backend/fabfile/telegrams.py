# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB

# Restrict visible functions
__all__ = ['run', 'run_query', 'run_scraper',
           'upload_dc_fs', 'upload_dc_urls', 'upload_rest_dc_fs']


# LOCAL PATHS
cwd = os.path.dirname(__file__)
scripts_path = os.path.join(cwd, '../scripts')
yaml_path = os.path.join(cwd, '../scripts/yaml')


@runs_once
def run():
    '''execute preprocessing tasks on the input datasets'''
    execute(run_query)
    execute(run_scraper)


@task
@runs_once
def upload_dc_fs():
    '''upload to document cloud from local fs'''
    with lcd(cwd):
        local('python %s/upload_fs_telegrams_dc.py -f %s' % (scripts_path,
                                                             'pdf2'))


@task
@runs_once
def upload_rest_dc_fs():
    '''upload to document cloud from local fs'''
    with lcd(cwd):
        # local('python %s/upload_rest_fs_telegrams.py -f %s' % (scripts_path,
        #                                                        'pdf1'))
        # local('python %s/upload_rest_fs_telegrams.py -f %s' % (scripts_path,
        #                                                        'pdf2'))
        # local('python %s/upload_rest_fs_telegrams.py -f %s' % (scripts_path,
        #                                                        'pdf3'))
        local('python %s/upload_rest_fs_telegrams.py -f %s' % (scripts_path,
                                                               'pdf4'))
        local('python %s/upload_rest_fs_telegrams.py -f %s' % (scripts_path,
                                                               'pdf5'))


@task
@runs_once
def upload_dc_urls():
    '''upload telegram urls to document cloud'''
    with lcd(cwd):
        local('python %s/upload_url_telegrams_dc.py -f %s' % (scripts_path,
                                                              'pdf5'))


@task
@runs_once
def run_query():
    '''save telegram table to csv file'''
    with lcd(cwd):
        local('datafreeze --db %s %s/telegrams.yaml' % (DB, yaml_path))


@task
@runs_once
def run_scraper():
    '''run scraper in parallel to get all the pdfs'''
    with lcd(cwd):
        local('python %s/scrape_telegrams.py' % (scripts_path))
