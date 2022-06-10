#!/usr/bin/python3

import dnf
import sys
import argparse

parser=argparse.ArgumentParser(
    description='''Remotely query the Mariner archive database about packages''')
parser.add_argument('--arch', type=str, default='x86_64', help='CPU Architecture: x86_64 or aarch64')
parser.add_argument('package', nargs='*', default=[1, 2, 3], help='Package name(s)')
args=parser.parse_args()

# If no argument is pass to the script
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

# [Woraround] Redirecting stderr to /dev/null for repo with no repodata/respomd.xml
f = open('/dev/null', 'w')
sys.stderr = f

cachedir = '_dnf_cache_dir'
arch = args.arch

base = dnf.Base()
conf = base.conf
conf.cachedir = cachedir
conf.substitutions['basearch'] = arch
conf.skip_if_unavailable = True


# Mariner 1.0
#version= float(1)

cm1_repos = ["base", "Microsoft", "coreui", "extras", "update"]
for cm1_repo in cm1_repos:
    repo_name = "Mariner1_" + cm1_repo
    base.repos.add_new_repo(repo_name, conf,
        baseurl=["https://packages.microsoft.com/cbl-mariner/1.0/prod/"+ cm1_repo + "/" + arch + "/rpms"])
base.fill_sack(load_system_repo=False)

result = base.sack.query().filter(name=sys.argv[1]).latest()
if result:
    for pkg in result:
        print('[Mariner 1.0] {} in {}'.format(pkg, pkg.reponame))
else:
        print('[Mariner 1.0] not found')

# Mariner 2.0
#version= float(2)

cm2_repos = ["base", "Microsoft", "extended", "extras", "nvidia"]
for cm2_repo in cm2_repos:
    repo_name = "Mariner2_" + cm2_repo
    base.repos.add_new_repo(repo_name, conf,
        baseurl=["https://packages.microsoft.com/cbl-mariner/2.0/prod/" + cm2_repo + "/" + arch])
base.fill_sack(load_system_repo=False)

result = base.sack.query().filter(name=sys.argv[1]).latest()
if result:
    for pkg in result:
        print('[Mariner 2.0] {} in {}'.format(pkg, pkg.reponame))
else:
        print('[Mariner 2.0] not found')
