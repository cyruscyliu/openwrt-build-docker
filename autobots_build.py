# -*- coding: utf-8 -*-
'''
This module provides the interface of this builder with autobots
'''

import os
from pathlib import Path
from datetime import datetime

COMPILE_PKG_PATH = './compile_package'
BUILD_PKG_PATH = './build_package'

def get_current_time_str():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def make_compile_docker(openwrt_ver):
    # check whether this version of openwrt is supported
    compile_path = Path(COMPILE_PKG_PATH) / openwrt_ver
    if not compile_path.exists():
        return None
    
    build_script = str((compile_path / 'build.sh').absolute())
    compile_script = str((compile_path / 'compile.sh').absolute())

    ret = os.system('cd %s && bash %s' % (str(compile_path.absolute()), build_script))
    if ret != 0:
        return None

    return compile_script

def make_build_package(target_dir, openwrt_ver, config_path, tag=None):
    os.system('mkdir -p %s' % (target_dir))

    # check whether this version of openwrt is supported
    build_pkg_path = Path(BUILD_PKG_PATH) / openwrt_ver
    if not build_pkg_path.exists():
        return None

    build_dir = None
    if tag != None:
        build_dir = Path(target_dir) / (openwrt_ver + '-' + tag)
    else:
        build_dir = Path(target_dir) / (openwrt_ver + '-' + get_current_time_str())
    
    ret = os.system('cp -r %s %s' % (build_pkg_path, build_dir))
    if ret != 0:
        return None
    
    ret = os.system('cp %s %s/OpenWrt.config' % (config_path, build_dir))
    if ret != 0:
        return None
    
    return str(build_dir.absolute())

def do_the_building(build_dir, compile_script):
    ret = os.system('bash %s %s' % (compile_script, build_dir))
    if ret != 0:
        return False
    
    return True

def one_work_flow(target_dir, openwrt_ver, config_path, build=False, tag=None):
    '''
    target_dir  : the compile & build package installation place
    openwrt_ver : ver of the openwrt
    config_path : openwrt config path
    build       : build after all packages are prepared
    '''
    compile_script = make_compile_docker(openwrt_ver)
    if compile_script == None:
        return False

    build_dir = make_build_package(target_dir, openwrt_ver, config_path, tag=tag)
    if build_dir == None:
        return False

    if build:
        print('hahaha', build_dir, compile_script)
        return do_the_building(build_dir, compile_script)
    
    return True