#!/usr/bin/env python
# -*- coding: utf-8 -*-

# fabfile.py

import os, re
from datetime import datetime

from fabric.api import *

# 服务器登录用户名
env.user = 'redye'
# sudo 用户为 root
env.sudo_user = 'root'
# 服务器地址，可以有多个，一次部署
env.hosts = ['172.19.40.96']

# 服务器 MySQL 用户名和口令
db_user = 'www-data'
db_password = 'www-data'

_TAR_FILE = 'dist-awesome.tar.gz'
_REMOTE_TMP_TAR = '/tmp/%s' % _TAR_FILE
_REMOTE_BASE_DIR = '/srv/awesome'

def _current_path():
	return os.path.abspath('.')

def _now():
	return datetime.now().strftime('%y-%m-%d_%H.%M.%S')

def build():
	includes = ['static', 'templates', 'favicon.ico', '*.py']
	excludes = ['test', '.*', '*.pyc', '*.pyo']
	local('rm -f dist/%s' % _TAR_FILE)
	with lcd(os.path.join(_current_path(), 'www')):
		cmd = ['tar', '--dereference', '-czvf', '../dist/%s' % _TAR_FILE]
		cmd.extend(['--exclude=\'%s\'' % ex for ex in excludes])
		cmd.extend(includes)
		local(' '.join(cmd))


def deploy():
	newdir = 'www-%s' % _now()
	# 删除已有的 tar 文件:
	run('rm -f %s' % _REMOTE_TMP_TAR)
	# 上传新的 tar 文件:
	put('dist/%s' % _TAR_FILE, _REMOTE_TMP_TAR)
	# 创建新目录：
	with cd(_REMOTE_BASE_DIR):
		sudo('mkdir %s' % newdir)
	# 解压到新目录
	with cd('%s/%s' % (_REMOTE_BASE_DIR, newdir)):
		sudo('tar -xzvf %s' % _REMOTE_TMP_TAR)
	# 重置软链接：
	with cd(_REMOTE_BASE_DIR):
		sudo('rm -r www')
		sudo('ln -s %s www' % newdir)   # 建立软链接 ln -s 源文件 目标文件
		sudo('chown www-data:www-data www')
		sudo('chown -R www-data:www-data %s' % newdir)
	# 重启 Python 服务和 ngnix 服务
	with settings(warn_only=True):
		sudo('supervisorctl stop awesome')
		sudo('supervisorctl start awesome')
		sudo('/etc/init.d/nginx start')    # 启动 ngnix 服务
		sudo('/etc/init.d/nginx reload')








































