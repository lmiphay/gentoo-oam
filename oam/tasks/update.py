# -*- coding: utf-8 -*-

from invoke import task
import oam.lib

""" Todo:
    strip ansi for python-updater (einfo) and perl-cleaner
    need regex filtering for python-updated and perl-cleaner
    add changed python and perl installs
    note: revdep-rebuild, python-updater and perl-cleaner have pretend support
    note: `emerge --rebuild-if-new-rev=y` doesn't appear to be useful for update pkg
"""

@task(name='update-available')
def update_available(ctx):
    with ctx.cd('/var/log/oam/latest'):
        return ctx.run("tail -n 7 sync.log | grep -q 'An update to portage is available'").ok

@task(name='update-package', aliases=['update-portage'])
def update_package(ctx, atom='sys-apps/portage'):
    ctx.emerge('--oneshot {}'.format(atom), if_new_rev=True)

@task(name='revdep-rebuild', aliases=['rr'])
def revdep_rebuild(ctx):
    ctx.run('/usr/bin/revdep-rebuild --nocolor --ignore', if_installed=True)

@task(name='python-updater', aliases=['pu'])
def python_updater(ctx):
    ctx.run('/usr/sbin/python-updater -eall', if_installed=True)

@task(name='perl-cleaner', aliases=['pc'])
def perl_cleaner(ctx):
    ctx.run('/usr/sbin/perl-cleaner --all', if_installed=True)
    
@task(name='preserved-rebuild', aliases=['pr'])
def preserved_rebuild(ctx, force=False):
    if force or oam.lib.preserved_libs():
        ctx.emerge('--keep-going @preserved-rebuild')

PRE = [update_package]
POST = [revdep_rebuild, python_updater, perl_cleaner, preserved_rebuild]

@task(default=True, pre=PRE, post=POST, aliases=['up'])
def update(ctx, target='world'):
    """note that if a problem is found in the pretend phase, then --keep-going 
       will not keep the build running (the pre-merge check will fail the update)
    """
    ctx.emerge('--update --keep-going {}'.format(target))
