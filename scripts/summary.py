#!/usr/bin/python
import os
import yaml
from multiprocessing import Pool


def worker(hash_of_image_builder, openwrtver, full_path):
    support_list = {
        'revision': openwrtver, 'full_path': full_path}

    # find makeout.txt
    makeout = os.popen(
        'cd {} && find -name makeout.txt'.format(full_path)).readlines()
    if len(makeout) > 0:
        support_list['path_to_makeout'] = \
            os.path.join(full_path, makeout[0].strip())

    # find vmlinux.elf-debug-info
    vmlinux_debug_results = os.popen(
        'cd {} && find -name vmlinux.elf-debug-info'.format(
            full_path)).readlines()
    set_vmlinux_debug = set([
        os.path.dirname(path) for path in vmlinux_debug_results])
    # find vmlinux
    vmlinux_results = os.popen(
        'cd {} && find -name vmlinux'.format(full_path)).readlines()
    set_vmlinux = set([
        os.path.dirname(os.path.dirname(path))
        for path in vmlinux_results])
    target_dirs = set_vmlinux_debug & set_vmlinux
    if len(target_dirs) == 0:
        print('[-] ignore unexpected vmlinux pattern in {}'.format(
            full_path))
        return

    # find .config
    dot_config_results = os.popen(
        'cd {} && find -name .config'.format(full_path)).readlines()
    set_config = set([
        os.path.dirname(os.path.dirname(path))
        for path in dot_config_results])
    target_dirs = target_dirs & set_config
    if len(target_dirs) == 0:
        print('[-] ignore unexpected .config pattern in {}'.format(
            full_path))
        return

    gcc = os.popen(
        'cd {} && find -name *-openwrt-linux-gcc'.format(full_path)).readlines()
    if len(gcc) > 0:
        support_list['path_to_gcc'] = \
            os.path.join(full_path, gcc[0].strip())

    # fill in support list
    target_dir = list(target_dirs)[0]
    # vmlinux.elf-debug-info
    for path in vmlinux_debug_results:
        if os.path.dirname(path) == target_dir:
            support_list[
                'path_to_vmlinux_debug_info'] = \
                os.path.join(full_path, path.strip())
    # source code
    for path in vmlinux_results:
        if os.path.dirname(os.path.dirname(path)) == target_dir and \
                os.path.basename(os.path.dirname(path)).find('linux') != -1:
            support_list['path_to_source_code'] = \
                os.path.join(full_path, os.path.dirname(path.strip()))
            support_list['path_to_vmlinux'] = \
                os.path.join(full_path, path.strip())
            support_list['path_to_dot_config'] = \
                os.path.join(full_path, os.path.join(
                    os.path.dirname(path.strip()), '.config'))
    yaml.safe_dump(
        support_list, open('.{}.yaml'.format(hash_of_image_builder), 'w'))
    print('[+] update support list for {}'.format(full_path))


def update_support_list():
    pool = Pool(20)

    for owver_ibhash in os.listdir('share'):
        full_path = os.path.join('share', owver_ibhash)
        if os.path.isfile(full_path):
            print('[-] ignore file {}'.format(owver_ibhash))
            continue

        items = owver_ibhash.split('-')
        if len(items) >= 3:
            hash_of_image_builder = '-'.join(items[2:])
        else:
            hash_of_image_builder = '-'.join(items[1:])

        if not len(hash_of_image_builder):
            print('[-] ignore invalid hash in {}'.format(owver_ibhash))
            continue
        if len(items) >= 3:
            # 17.01.0-rc1-07f1
            openwrtver = '-'.join(items[:2])
        else:
            # 17.01.1-017c
            openwrtver = items[0]

        pool.apply_async(
            worker, args=(hash_of_image_builder, openwrtver, full_path))
    pool.close()
    pool.join()

    support_list = {}
    for saved_support_info in os.listdir('.'):
        if saved_support_info.startswith('.') and \
                saved_support_info.endswith('yaml'):
            support_info = yaml.safe_load(open(saved_support_info))
            hash_of_image_builder = saved_support_info[1:-5]
            support_list[hash_of_image_builder] = support_info
            os.system('rm {}'.format(saved_support_info))

    yaml.safe_dump(support_list, open('summary.yaml', 'w'))


if __name__ == '__main__':
    update_support_list()
