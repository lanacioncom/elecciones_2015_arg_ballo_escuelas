# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
from settings import DB

# Restrict visible functions
__all__ = ['run', 'run_query', 'run_scraper',
           'upload_dc_fs', 'upload_dc_urls', 'upload_rest_dc_fs',
           'delete_dc_docs', 'get_project_dc_docs']


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
        local('python %s/telegrams_upload_fs_dc.py -f %s' % (scripts_path,
                                                             'pdf1'))


@task
@runs_once
def upload_rest_dc_fs():
    '''upload to document cloud from local fs'''
    with lcd(cwd):
        local('python %s/telegrams_upload_rest_fs.py -f %s' % (scripts_path,
                                                               'pdf1'))


@task
@runs_once
def upload_dc_urls():
    '''upload telegram urls to document cloud'''
    with lcd(cwd):
        local('python %s/telegrams_upload_url_dc.py -f %s' % (scripts_path,
                                                              'pdf5'))


@task
@runs_once
def delete_dc_docs():
    '''delete document cloud docs based on csv with ids'''
    with lcd(cwd):
        local('python %s/telegrams_delete_dup_dc.py -f %s' % (scripts_path,
                                                              'duplicates'))


@task
@runs_once
def get_project_dc_docs(proj=None):
    '''get document cloud docs from project passed by arguments to the task'''
    f = "proj_%s_docs" % (proj)
    with lcd(cwd):
        local('python %s/telegrams_get_proj_docs_dc.py -p %s -f %s' % (
            scripts_path,
            proj,
            f))


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
        local('python %s/telegrams_scrape.py' % (scripts_path))
