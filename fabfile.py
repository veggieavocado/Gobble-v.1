'''
****** TASK MANAGER USING FABRIC/PYTHON ******

RUN: "fab <taskname>"
(ex) fab shell
(the tasknames are defined below, check the codes below for more information)

###### LOCAL FAB TASKS ######
==> can run on local computer/servers
shell
runserver
static
new_static
migrate
full_migrate
test
lazy_commit
clean_known_hosts
send_crypt_key
'''

import os
from fabric.api import *

from cryptography.fernet import Fernet
from molecular.settings import IP_ADDRESS

local_ip = '127.0.0.1'


###### LOCAL FAB TASKS ######
@task
@hosts(local_ip)
def shell():
    # opens the shell
    local('python manage.py shell')

@task
@hosts(local_ip)
def runserver():
    # runs the Django server
    local('python manage.py runserver')

@task
@hosts(local_ip)
def static():
    # collects static files again
    local('python manage.py collectstatic')

@task
@hosts(local_ip)
def new_static():
    # removes static-dist directory and collects static again
    local('rm -r static-dist')
    local('mkdir static-dist')
    local('python manage.py collectstatic')

@task
@hosts(local_ip)
def migrate():
    # make migrations on DB then migrate those changes
    local('python manage.py makemigrations')
    local('python manage.py migrate')

@task
@hosts(local_ip)
def full_migrate():
    local('python manage.py makemigrations auth')
    local('python manage.py makemigrations accounts')
    local('python manage.py makemigrations services')
    local('python manage.py migrate')

@task
@hosts(local_ip)
def test():
    # perform Django tests
    local('python manage.py test')

@task
@hosts(local_ip)
def lazy_commit(commit_msg):
    # git add . > git commit then git pushes changes lazily
    with settings(warn_only=True):
        local('git add -A')
        local('git commit -m "{}"'.format(commit_msg))
    local('git push')

@task
@hosts(local_ip)
def clean_known_hosts():
    # for mac users
    # delete all known host records
    local('echo "" > /Users/abc/.ssh/known_hosts')

@task
@hosts(IP_ADDRESS)
def send_crypt_key():
    # 크립트키 서버로 보내기
    env.user = 'root'
    put('./molecular/crypt_key.py', '~/Gobble-VA/molecular/crypt_key.py')
