# -*- coding: utf-8 -*-

import os.path
import re

from invoke import task

"""
1. host: generate list of packages (manifest) to build on the host
2. container: configure to match the host
    a. /etc/portage/make.conf (CPPFLAGS/LDFLAGS, ACCEPT_LICENSE, use flags...)
    b. /etc/portage/package.use
    c. /etc/portage/package.provided (e.g. may want to provide kernel sources)
    d. /etc/portage/package.keywords for relevant packages
    d. depclean the container (optional)
3. container: bring up to date (inc newuse) (check /usr/portage/packages is writable from container)
4. container: parse list and build a binary package of anything which is not already available as a binary package
5. host: install the binary packages
"""

PKGDIR = os.getenv('PKGDIR', '/usr/portage/packages')
BUILD_OPT = '-1 --verbose --verbose-conflicts --keep-going --buildpkg=y'
INSTALL_OPT = '-1 --usepkgonly=y --nodeps --verbose --binpkg-changed-deps=y --with-bdeps=n'

def pkg_exists(atom):
    return os.path.isfile('{}/{}.tbz2'.format(PKGDIR, atom))

def packages(manifest):
    """ convert:
           [ebuild   R    ] dev-libs/liborcus-0.11.2  PYTHON_SINGLE_TARGET="(-python3_6)" PYTHON_TARGETS="(-python3_6)" 
        to:
           dev-libs/liborcus-0.11.2
    """
    for line in open(manifest, 'r').readlines():
        if line.startswith('[ebuild'):
            yield re.sub(r'^\[[^]]+\] ([^: ]+).*', r'\1', line.strip())

def unbuilt(manifest):
    """yields a list of packages which have not yet been built"""
    for atom in packages(manifest):
        if not pkg_exists(atom):
            print 'Will-build: ', atom
            yield atom
        else:
            print 'Already-built: ', atom

@task
def manifest(ctx):
    """host: generate list of packages to rebuild
       see: new item from 2015-10-22: GCC 5 Defaults to the New C++11 ABI
    """
    ctx.run("revdep-rebuild --pretend --library 'libstdc++.so.6' -- --exclude gcc")

@task
def update(ctx):
    """container: update to match host use setting"""
    ctx.run('emerge --update --newuse --deep --verbose world')

@task
def build(ctx, manifest):
    """container: build packages"""
    ctx.run('emerge --pretend {} ={}'.format(BUILD_OPT, ' ='.join(unbuilt(manifest))), echo=True)

@task
def install(ctx, manifest):
    """host: install packages"""
    ctx.run('emerge {} {}'.format(INSTALL_OPT, ' ='.join(packages(manifest))), echo=True)


