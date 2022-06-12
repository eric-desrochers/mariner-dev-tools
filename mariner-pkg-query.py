#!/usr/bin/python3

__author__ = "Eric Desrochers"
__maintainer = "Eric Desrochers"
__version__ = "1.0"
__status__ = "Development"

import dnf
import sys
import argparse
from prettytable import PrettyTable

parser=argparse.ArgumentParser(
    description='''Remotely query the Mariner archive database about packages''')
parser.add_argument('package', nargs=1, help='Package name')
args=parser.parse_args()

# If no argument is pass to the script
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# [Workaround] Redirecting stderr to /dev/null for repo with no repodata/respomd.xml
f = open('/dev/null', 'w')
sys.stderr = f

# Setting up the cache
cachedir = '_dnf_cache_dir'

# Configuration
base = dnf.Base()
conf = base.conf
conf.cachedir = cachedir
conf.skip_if_unavailable = True

# Prettytable
myTable = PrettyTable(["Mariner", "Name", "DebugInfo", "Version", "Arch", "Repo"])

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
            repo = pkg.reponame.split("_")
            myTable.add_row([cmver, pkg.name, pkg.debug_name, pkg.evr, pkg.arch, repo[-1]])
    else:
            myTable.add_row([cmver,"Not found", "X", "X", "X", "X"])

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

    result = base.sack.query().filter(name=sys.argv[1]).available().latest()
    if result:
        for pkg in result:
            repo = pkg.reponame.split("_")
            myTable.add_row([cmver, pkg.name, pkg.debug_name, pkg.evr, pkg.arch, repo[-1]])
    else:
            myTable.add_row([cmver,"Not found", "X", "X", "X", "X"])

def reporting():
    """
    Prettytable format reporting
    """
    print(myTable)

# Executing functions
cm1()
cm2()
reporting()
