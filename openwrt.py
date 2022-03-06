#!/usr/bin/python3
import os
import re
import sys
import json
import utils
import argparse
import importlib

from pathlib import Path
from libopenwrt import one_work_flow

BUILD_DIR = "build"
PACKAGES = "packages"

OPENWRT_CFG_DB_TAR_XZ = "%s/openwrt_config_database.tar.xz" % (PACKAGES)
OPENWRT_CFG_DB = "%s/openwrt_config_database" % (PACKAGES)
BDINFO_TABLE = "%s/bdinfo_table_builder.json" % (PACKAGES)

build_switch = True


def __make_build_env(args):
    openwrt_ver, config_path, tag = args
    print('[+] Making build env for %s in %s using cfg %s' % (tag, openwrt_ver, config_path))

    # choose the supported openwrt version
    ver = re.search('[0-9]+\\.[0-9]+(\\.[0-9]+(-rc[0-9])?)?$', openwrt_ver).group(0)
    if ver == None:
        return tag, False, ('could not extract version of openwrt %s for %s' % (openwrt_ver, tag))

    succ = one_work_flow(BUILD_DIR, ver, config_path, build=build_switch, tag=tag)
    return tag, succ, ''


def __load_the_openwrt_cfg_db():
    if not os.path.exists(OPENWRT_CFG_DB):
        os.system('tar Jxf {} -C {}'.format(OPENWRT_CFG_DB_TAR_XZ, PACKAGES))


def __load_the_bdinfo_table():
    """
    0            1       2          3           4      5
    openwrt_ver, target, subtarget, kernel_ver, board, i.o.k.t,
    6        7            8           9
    builder, openwrt cfg, kernel cfg, device tree
    """
    if not os.path.exists(BDINFO_TABLE):
        return None

    with open(BDINFO_TABLE, 'r') as f:
        table = json.loads(f.read(-1))

    bdinfo_table = {}

    for row in table:
        openwrt_ver, target, subtarget, _, _, _, _, _, _, _, _ = row
        if bdinfo_table.get(openwrt_ver, None) == None:
            bdinfo_table[openwrt_ver] = {}
        if bdinfo_table[openwrt_ver].get(target, None) == None:
            bdinfo_table[openwrt_ver][target] = {}
        if bdinfo_table[openwrt_ver][target].get(subtarget, None) == None:
            bdinfo_table[openwrt_ver][target][subtarget] = None
        bdinfo_table[openwrt_ver][target][subtarget] = row
    return bdinfo_table


def make_build_env_by_subtarget(over_patts, tar_patts, subtar_patts, dumpto=None):
    """
    openwrt_ver, target, subtarget receives regex pattern string as input
    """
    __load_the_openwrt_cfg_db()

    table = __load_the_bdinfo_table()
    if table is None:
        print('[-] please run download.sh first, %s is missing' % BDINFO_TABLE)
        exit(-1)

    matches = []
    task_list = []
    status_of_rslts = {}

    # 1. find matches
    M = lambda patt, d: [ k for k in d.keys() if re.search(patt, k) != None ]
    if len(over_patts) != len(tar_patts) or len(over_patts) != len(subtar_patts):
        print('[-] patterns length does not match (operwrt revision %s target %s subtarget %s)' %
              (len(over_patts), len(tar_patts), len(subtar_patts)))
        return
    for idx in range(0, len(over_patts)):
        for over in M(over_patts[idx], table):
            for target in M(tar_patts[idx], table[over]):
                for subtarget in M(subtar_patts[idx], table[over][target]):
                    row = (over, target, subtarget)
                    matches.append(row)
    print('[+] find %s matches' %(len(matches)))

    # 2. sieve matches by the bdinfo table (i.o.k.t)
    for over, target, subtarget in matches:
        ty = table[over][target][subtarget][10]
        key = '%s-%s-%s-%s' % (over, target, subtarget, ty)
        _, o, _, _ = table[over][target][subtarget][5].split('.')
        ocfg = table[over][target][subtarget][7]
        if o != 't':
            status_of_rslts[key] = (False, 'not supported due to the lack of openwrt config %s', o)
        else:
            print('[+] verbose: %s %s %s %s' % (over, target, subtarget, ocfg))
            ocfg = str((Path(OPENWRT_CFG_DB) / ocfg).absolute())
            task_list.append((over, ocfg, key))
    print('[+] after sieve, %s matches' % (len(task_list)))

    # 3. build_env in parallel
    def handle_result(rslt_list):
        for rslt in rslt_list:
            key, succ, err = rslt
            status_of_rslts[key] = (succ, err)

    utils.do_in_parallel(__make_build_env, task_list, handle_result, para=1)

    # 3. dump all results
    if dumpto == None:
        for key, (succ, err) in status_of_rslts.items():
            if not succ:
                print('[+] FAIL: key %s, %s' % (key, err))
    else:
        with open(dumpto, 'a') as f:
            f.write('--------------------------\n')
            for key, (succ, err) in status_of_rslts.items():
                if not succ:
                    f.write('FAIL: key %s, %s\n' % (key, err))
                else:
                    f.write('SUCC: key %s\n' % (key))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("listfile", action="store",
                      help="version target subtarget list")
    parser.add_argument("-t", "--try-1st", dest="is_try", default=False,
                      help="try the first line of the list", action="store_true")
    parser.add_argument("-s", "--skip_build", dest="skipbuild", default=False,
                      help="test but skip the build process", action="store_true")
    parser.add_argument("-o", "--logout", dest="logfile", default=None,
                      help="append log file, by default stdout")
    options = parser.parse_args()

    if options.skipbuild:
        build_switch = False

    overs, tars, subtars = [], [], []
    with open(options.listfile, 'r') as f:
        line_num = 0
        for line in f.readlines():
            line_num = line_num + 1
            line = line.strip()
            if not line.startswith('#'):
                parts = line.split(' ')
                if len(parts) != 3:
                    print('[+] The listfile %s line %d should follow the format "var tar subtar"' % (options.listfile, line_num))
                    exit(-1)
                overs.append(parts[0].strip())
                tars.append(parts[1].strip())
                subtars.append(parts[2].strip())
    if options.is_try:
        overs, tars, subtars = [overs[0]], [tars[0]], [subtars[0]]
    make_build_env_by_subtarget(overs, tars, subtars, dumpto=options.logfile)
