#!/usr/bin/python3

import dnf
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Remotely query the Mariner archive database about packages''')
parser.add_argument('package', nargs='*', default=[1, 2, 3], help='Package name(s)')
args=parser.parse_args()

# If no argument is pass to the script
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# [Workaround] Redirecting stderr to /dev/null for repo with no repodata/respomd.xml
f = open('/dev/null', 'w')
sys.stderr = f

cachedir = '_dnf_cache_dir'

base = dnf.Base()
conf = base.conf
conf.cachedir = cachedir
conf.skip_if_unavailable = True

def cm1():
    """
    Function to find package in Mariner 1.0
    """

    cmver = float(1)
    cm1_repos = ["base", "Microsoft", "coreui", "extras", "update"]
    for cm1_repo in cm1_repos:
        x86repo_name = "x86_64_cm1_" + cm1_repo
        arm64repo_name = "arm64_cm1_" + cm1_repo
        base.repos.add_new_repo(x86repo_name, conf,
            baseurl=["https://packages.microsoft.com/cbl-mariner/1.0/prod/"+ cm1_repo + "/" + "x86_64" + "/rpms"])
        base.repos.add_new_repo(arm64repo_name, conf,
            baseurl=["https://packages.microsoft.com/cbl-mariner/1.0/prod/"+ cm1_repo + "/" + "aarch64" + "/rpms"])
    base.fill_sack(load_system_repo=False)

    result = base.sack.query().filter(name=sys.argv[1]).available().latest()
    if result:
        for pkg in result:
            print('| Mariner {} | {}\t| {}\t| {}\t| {}'.format(cmver, pkg.name,pkg.version,pkg.arch, pkg.reponame))
    else:
            print('| Mariner {} | not found'.format(cmver))

def cm2():
    """
    Function to find package in Mariner 1.0
    """

    cmver = float(2)
    cm2_repos = ["base", "Microsoft", "extended", "extras", "nvidia"]
    for cm2_repo in cm2_repos:
        x86repo_name = "x86_64_cm2_" + cm2_repo
        arm64repo_name = "arm64_cm2_" + cm2_repo
        base.repos.add_new_repo(x86repo_name, conf,
            baseurl=["https://packages.microsoft.com/cbl-mariner/2.0/prod/" + cm2_repo + "/" + "x86_64"])
        base.repos.add_new_repo(arm64repo_name, conf,
            baseurl=["https://packages.microsoft.com/cbl-mariner/2.0/prod/" + cm2_repo + "/" + "aarch64"])
    base.fill_sack(load_system_repo=False)

    result = base.sack.query().filter(name=sys.argv[1]).latest()
    if result:
        for pkg in result:
            print('| Mariner {} | {}\t| {}\t| {}\t| {}'.format(cmver, pkg.name,pkg.version,pkg.arch, pkg.reponame))
    else:
            print('| Mariner {} | not found'.format(cmver))

# Executing functions
cm1()
cm2()
