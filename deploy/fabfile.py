# coding: utf-8
from __future__ import with_statement
from fabric.api import *
from fabric.utils import abort
import os
import shutil
import time

# Restrict visible functions
__all__ = ['default', 'deploy', 'test_deploy10', 'test_deploy11',
           'umount', 'mount']

# LOCAL PATHS
cwd = os.path.dirname(__file__)


def validate():
    '''validate the deployment sources prior to actually deploy'''
    build_path = os.path.join(cwd, '../build')
    if not os.path.exists(build_path):
        msg = 'There is no built project to deploy.\n' \
              'First generate the production ready project and then rerun'
        abort(msg)
    if not os.listdir(build_path):
        msg = 'The built project is empty.\n' \
              'First generate the production ready project and then rerun'
        abort(msg)
    parent_path = os.environ.get('SERVER_PARENT_PATH', None)
    if not parent_path:
        msg = 'The deployment process needs a server parent folder to run.\n' \
              'Set up SERVER_PARENT_PATH env var accordingly and rerun'
        abort(msg)


# DEPLOY TO ESPECIALES PRODUCCION
@task
def mount_esp(server_ix='10'):
    '''mount especiales server into local disk'''
    SAMBA_MNT = os.environ.get(
        'SAMBA_CONN%s' % (server_ix),
        "sudo -u user command smb://'DOMAIN;user':pass@SERVER/dir")
    local_path = os.path.join(cwd, 'mnt%s' % (server_ix))
    # Create folder structure on the mounted server
    if os.path.exists(local_path):
        shutil.rmtree(local_path)
    os.makedirs(local_path)
    with hide('everything'), settings(warn_only=True):
        result = local('%s/proyectos/ %s'
                       % (SAMBA_MNT, local_path), capture=True)
    if result.succeeded:
        msg = "server %(srv)s mounted on mnt%(srv)s" % {'srv': server_ix}
        puts(msg, flush=True)
    else:
        msg = 'Failed to mount server %s. Reason %s' % (server_ix,
                                                        result.stderr)
        abort(msg)


@task
def umount_esp(server_ix='10'):
    with lcd(cwd):
        with hide('everything'), settings(warn_only=True):
            result = local('umount mnt%s' % (server_ix), capture=True)
        if result.succeeded:
            msg = "server %(srv)s unmounted from mnt%(srv)s" % {
                'srv': server_ix}
            puts(msg, flush=True)
        else:
            msg = 'Failed to unmount server %s. Reason %s' % (server_ix,
                                                              result.stderr)
            puts(msg, flush=True)


@task
def deploy_esp(server_ix='10', test=False):
    '''deploy build to especiales server'''
    validate()
    # If validation succeeds
    build_path = os.path.join(cwd, '../build')
    parent_path = os.environ.get('SERVER_PARENT_PATH')
    # Testing?
    if test:
        dest_path = os.path.join(parent_path, 'tmp_fabric')
    else:
        project_folder = os.environ.get('PROJECT_FOLDER')
        # Project folder not set use default which is the parent folder
        if not project_folder:
            # Derive the project name from the parent folder name
            project_folder = os.path.basename(os.path.abspath(os.path.join(cwd,
                                                              '../')))
            msg = "project_folder: %s" % (project_folder)
            puts(msg, flush=True)

        dest_path = os.path.join(parent_path, project_folder)

    # mount especiales server
    mounted_path = os.path.join(cwd, 'mnt%s' % (server_ix))
    if not os.path.ismount(mounted_path):
        execute(umount_esp, server_ix=server_ix)
        # Let it rest just a bit
        time.sleep(1)
        execute(mount_esp, server_ix=server_ix)

    mnt_dest_path = os.path.join(mounted_path, dest_path)

    # Create destination folder if needed
    if not os.path.exists(mnt_dest_path):
        os.makedirs(mnt_dest_path)

    local('cp -v -r %s/* %s'
          % (build_path, mnt_dest_path))

    # Let it rest just a bit
    time.sleep(2)
    # unmount especiales server
    execute(umount_esp, server_ix=server_ix)


@task
def mount():
    '''unmount folders especiales 10 & 11'''
    execute(mount_esp, server_ix='10')
    execute(mount_esp, server_ix='11')


@task
def umount():
    '''unmount folders especiales 10 & 11'''
    execute(umount_esp, server_ix='10')
    execute(umount_esp, server_ix='11')


@task
def deploy():
    '''deploy build to especiales 10 & 11'''
    execute(deploy_esp, server_ix='10')
    # execute(deploy_esp, server_ix='11')


@task
def test_deploy10():
    '''test deploy to especiales 10 tmp_fabric folder'''
    execute(deploy_esp, server_ix='10', test=True)


@task
def test_deploy11():
    '''test deploy to especiales 11 tmp_fabric folder'''
    execute(deploy_esp, server_ix='11', test=True)


# DEFAULT TASK
@task(default=True)
def default():
    '''list all fabric tasks'''
    local('fab --list')
