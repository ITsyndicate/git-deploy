# -*- coding: utf-8 -*-
__author__ = 'ibis'

from bottle import request, post, run
import os, shutil
from git.cmd import Git
from git import Repo


#Settings section
WEBROOT = '/tmp/repos'


@post('/deploy')
def deploy():
    git_info = request.json
    print git_info
    #Get info about repo
    refs = git_info['ref']
    before = git_info['before']
    after = git_info['after']
    url = git_info['repository']['url']
    remote_name = git_info['repository']['name']
    remote_branch = refs.split('/')[2]
    repopath = '{webroot}/{project}/{branch}'.format(
        webroot=WEBROOT, project=remote_name, branch=remote_branch
    )
    #Check, if branch already created under webroot
    if not os.path.exists(repopath):
        os.makedirs(repopath)
        new_repo = Repo.clone_from(url=url,to_path=repopath)
        git = new_repo.git
        git.checkout(remote_branch)
    elif after == u'0000000000000000000000000000000000000000':
        #We recive push with delete branch
        shutil.rmtree(repopath)
    else:
        #Update corresponding repo
        repo = Repo(repopath)
        origin = repo.remotes.origin
        origin.pull()





if __name__ == "__main__":
    run(host='0.0.0.0', port=8080)
