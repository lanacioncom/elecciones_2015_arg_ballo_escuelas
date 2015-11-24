# coding: utf-8
from __future__ import with_statement
from fabric.api import *
import os
import shutil
import time

# Restrict visible functions
__all__ = ['default', 'deploy', 'test_deploy10', 'test_deploy11']

# LOCAL PATHS
cwd = os.path.dirname(__file__)


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

    local('%s/proyectos/ %s'
          % (SAMBA_MNT, local_path))


@task
def umount_esp(server_ix='10'):
    with lcd(cwd):
        with settings(warn_only=True):
            local('umount mnt%s' % (server_ix))


@task
def deploy_esp(server_ix='10'):
    '''deploy build to especiales server'''
    build_path = os.path.join(cwd, '../build')
    tmp_path = os.environ.get('TMP_PATH', 'tmp')
    project_path = os.environ.get('PROJECT_PATH', 'tmp')
    # mount especiales server
    mounted_path = os.path.join(cwd, 'mnt%s' % (server_ix))
    if not os.path.exists('%s/15' % (mounted_path)):
        execute(umount_esp, server_ix=server_ix)
        execute(mount_esp, server_ix=server_ix)

    mnt_tmp_path = os.path.join(mounted_path, tmp_path)
    mnt_project_path = os.path.join(mounted_path, project_path)

    # Create destination folder if needed
    if not os.path.exists(mnt_project_path):
        os.makedirs(mnt_project_path)

    local('cp -v -r %s/* %s'
          % (build_path, mnt_project_path))

    # Let it rest just a bit
    time.sleep(2)
    # unmount especiales server
    execute(umount_esp, server_ix=server_ix)


@task
def test_deploy_esp(server_ix='10'):
    '''deploy build to especiales server'''
    build_path = os.path.join(cwd, '../build')
    tmp_path = os.environ.get('TMP_PATH', 'tmp')
    # mount especiales server
    mounted_path = os.path.join(cwd, 'mnt%s' % (server_ix))
    if not os.path.exists('%s/15' % (mounted_path)):
        execute(umount_esp, server_ix=server_ix)
        execute(mount_esp, server_ix=server_ix)

    mnt_tmp_path = os.path.join(mounted_path, tmp_path)

    # Clear out and recreate tmp folder if it exists
    if os.path.exists(mnt_tmp_path):
        shutil.rmtree(mnt_tmp_path)
    os.makedirs(mnt_tmp_path)

    local('cp -v -r %s/* %s'
          % (build_path, mnt_tmp_path))

    # Let it rest just a bit
    time.sleep(2)
    # unmount especiales server
    execute(umount_esp, server_ix=server_ix)


@task
def umount():
    '''unmount folders especiales 10 & 11'''
    execute(umount_esp, server_ix='10')
    execute(umount_esp, server_ix='11')


@task
def deploy():
    '''deploy build to especiales 10 & 11'''
    execute(deploy_esp, server_ix='10')
    execute(deploy_esp, server_ix='11')


@task
def test_deploy10():
    '''test deploy to especiales 10 tmp_fabric folder'''
    execute(test_deploy_esp, server_ix='10')


@task
def test_deploy11():
    '''test deploy to especiales 11 tmp_fabric folder'''
    execute(deploy_esp, server_ix='11')


# DEFAULT TASK
@task(default=True)
def default():
    '''list all fabric tasks'''
    local('fab --list')
