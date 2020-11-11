"""
This module provides the interface of this builder with autobots
"""
import os
from pathlib import Path
from datetime import datetime


WORK_BASE = 'packages'
COMPILE_PKG_PATH = WORK_BASE + '/compile_package'
BUILD_PKG_PATH = WORK_BASE + '/build_package'


def get_current_time_str():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def make_compile_docker(openwrt_ver):
    global COMPILE_PKG_PATH

    # for compile, currently we believe xx.xx is enough
    openwrt_ver = '.'.join(openwrt_ver.split('.')[0:2])

    # check whether this version of openwrt is supported
    compile_path = Path(COMPILE_PKG_PATH) / openwrt_ver
    if not compile_path.exists():
        print('[+] Error compile_path %s not exist' % (compile_path))
        return None

    build_script = str((compile_path / 'build.sh').absolute())
    compile_script = str((compile_path / 'compile.sh').absolute())

    ret = os.system('cd %s && bash -e %s' % (str(compile_path.absolute()), build_script))
    if ret != 0:
        print('[+] Error compile docker build_script %s returns non-zero' % (build_script))
        return None

    return compile_script


def make_build_package(target_dir, openwrt_ver, config_path, tag=None):
    global BUILD_PKG_PATH

    # for build, we believe we need all xx.xx[.xx[-rcx]]
    openwrt_ver = openwrt_ver

    # check whether this version of openwrt is supported
    build_pkg_path = Path(BUILD_PKG_PATH) / openwrt_ver
    if not build_pkg_path.exists():
        print('[+] build_pkg_path %s not exist' % (build_pkg_path))
        return None

    build_dir = None
    if tag != None:
        build_dir = Path(target_dir) / (openwrt_ver + '-' + tag)
    else:
        build_dir = Path(target_dir) / (openwrt_ver + '-' + get_current_time_str())

    ret = os.system('mkdir -p %s' % (build_dir))
    if ret != 0:
        print('[+] mkdir for %s error with ret %s' % (build_dir, ret))
        return None

    ret = os.system('cp -r %s/* %s' % (build_pkg_path, build_dir))
    if ret != 0:
        print('[+] copy build_pkg_path %s to build_dir %s error with ret %s' % (build_pkg_path, build_dir, ret))
        return None

    ret = os.system('cp %s %s/OpenWrt.config' % (config_path, build_dir))
    if ret != 0:
        print('[+] copy config %s to build_dir %s error with ret %s' % (config_path, build_dir, ret))
        return None

    return str(build_dir.absolute())


def do_the_building(build_dir, compile_script):
    with open(str((Path(build_dir) / 're_compile.sh').absolute()), 'w') as f:
        compile_str = '#!/bin/bash\nCOMPOSE_HTTP_TIMEOUT=120 docker-compose -f docker-compose.yml run --rm firmware-build\n'
        f.write(compile_str)

    compile_log = str((Path(build_dir) / 'compile.log').absolute())

    ret = os.system('bash -e %s %s > %s 2>&1' % (compile_script, build_dir, compile_log))
    if ret != 0:
        print('[+] Error compile_script %s returns non-zero' % (compile_script))
        return False

    return True


def one_work_flow(target_dir, openwrt_ver, config_path, build=False, tag=None):
    """
    target_dir  : the compile & build package installation place
    openwrt_ver : ver of the openwrt
    config_path : openwrt config path
    build       : build after all packages are prepared
    """
    compile_script = make_compile_docker(openwrt_ver)
    if compile_script == None:
        print('[+] Error compile_script is None')
        return False

    build_dir = make_build_package(target_dir, openwrt_ver, config_path, tag=tag)
    if build_dir == None:
        print('[+] Error build_dir is None')
        return False

    if build:
        return do_the_building(build_dir, compile_script)

    return True


def change_work_base(base):
    global WORK_BASE
    global COMPILE_PKG_PATH
    global BUILD_PKG_PATH

    WORK_BASE = base
    COMPILE_PKG_PATH = WORK_BASE + '/compile_package'
    BUILD_PKG_PATH = WORK_BASE + '/build_package'
