#!/usr/bin/python
"""
We are going to build machines in machines.csv.
"""
import os
import sys
import errno
import hashlib
from pyquery import PyQuery as pq


def find_urls_in_openwrt_homepage(homepage):
    """
    The url for ImageBuilder must include "ImageBuilder".
    The url for config includes, OpenWrt.config(10.03), config.diff(15.05).
    """
    html = pq(url=homepage)
    a = html('a')
    image_builder = None
    dot_config = None
    for item in a.items():
        href = item.attr('href')
        if image_builder is None and href.find('ImageBuilder') != -1:
            image_builder = os.path.join(homepage, href)
        if dot_config is None and (href.find('config.diff') != -1 or href.find('OpenWrt.config') != -1):
            dot_config = os.path.join(homepage, href)
    return image_builder, dot_config

def build_hash_of_url_to_image_builder():
    header = None
    image_builder_table = {}
    with open('machines.csv') as f:
        for line in f:
            items = line.strip().split(',')
            if header is None:
                header = items
                continue
            uuid = items[header.index('id')]
            url = items[header.index('url')]
            homepage = os.path.dirname(url)
            url_to_image_builder, _ = find_urls_in_openwrt_homepage(homepage)
            hash_of_image_builder = hashlib.md5(url_to_image_builder.encode('utf-8'))
            if hash_of_image_builder.hexdigest() in image_builder_table:
                # we also found many firmware share the same ImageBuilder
                # because they are downloaded from the same page
                image_builder_table[hash_of_image_builder.hexdigest()]['support'].append(uuid)
            else:
                image_builder_table[hash_of_image_builder.hexdigest()] = {'url': url_to_image_builder, 'support': [uuid]}
    return image_builder_table


def build(search=False):
    # 6. write all to support_list.csv
    if search:
        support_list = {}
        for one_building_dir in os.listdir('share'):
            full_path = os.path.join('share', one_building_dir)
            if os.path.isfile(full_path):
                continue
            openwrtver, _, hash_of_image_builder = one_building_dir.partition('-')
            if not len(hash_of_image_builder):
                continue
            # find vmlinux.elf-debug-info
            vmlinux_debug_results = os.popen('cd {} && find -name vmlinux.elf-debug-info'.format(full_path)).readlines()
            set_vmlinux_debug = set([os.path.dirname(path) for path in vmlinux_debug_results])
            # find vmlinux
            vmlinux_results = os.popen('cd {} && find -name vmlinux'.format(full_path)).readlines()
            set_vmlinux = set([os.path.dirname(os.path.dirname(path)) for path in vmlinux_results])
            target_dirs = set_vmlinux_debug & set_vmlinux
            if not len(target_dirs):
                continue
            # find .config
            dot_config_results = os.popen('cd {} && find -name .config'.format(full_path)).readlines()
            set_config = set([os.path.dirname(os.path.dirname(path)) for path in dot_config_results])
            target_dirs = target_dirs & set_config
            if not len(target_dirs):
                continue
            # fill in support list
            support_list[hash_of_image_builder] = {}
            target_dir = list(target_dirs)[0]
            # vmlinux.elf-debug-info
            for path in vmlinux_debug_results:
                if os.path.dirname(path) == target_dir:
                    support_list[hash_of_image_builder]['path_to_vmlinux_debug_info'] = os.path.join(full_path, path.strip())
            # source code
            for path in vmlinux_results:
                if os.path.dirname(os.path.dirname(path)) == target_dir and os.path.basename(os.path.dirname(path)).find('linux') != -1:
                    support_list[hash_of_image_builder]['path_to_source_code'] = os.path.join(full_path, os.path.dirname(path.strip()))
                    support_list[hash_of_image_builder]['path_to_vmlinux'] = os.path.join(full_path, path.strip())
                    support_list[hash_of_image_builder]['path_to_dot_config'] = os.path.join(full_path, os.path.join(os.path.dirname(path.strip()), '.config'))

        old_support_list = {}
        if os.path.exists('support_list.csv'):
            with open('support_list.csv', 'r') as f:
                for line in f:
                    hash_of_image_builder, vmlinux_debug_info, source_code, vmlinux, dot_config = line.strip().split(',')
                    if hash_of_image_builder in support_list:
                        continue
                    old_support_list[hash_of_image_builder] = {
                            'path_to_vmlinux_debug_info': vmlinux_debug_info,
                            'path_to_source_code': source_code,
                            'path_to_vmlinux': vmlinux,
                            'path_to_dot_config': dot_config
                    }

        with open('support_list.csv', 'w') as f:
            for h, v in old_support_list.items():
                f.write(','.join([h, v['path_to_vmlinux_debug_info'], v['path_to_source_code'], v['path_to_vmlinux'], v['path_to_dot_config']]))
                f.write('\n')
            for h, v in support_list.items():
                f.write(','.join([h, v['path_to_vmlinux_debug_info'], v['path_to_source_code'], v['path_to_vmlinux'], v['path_to_dot_config']]))
                f.write('\n')

        exit(0)


    # we found a .config always in an ImageBuilder
    if not os.path.exists('image_builder.csv'):
        image_builder_table = build_hash_of_url_to_image_builder()
        # save image_builder_table
        with open('image_builder.csv', 'w') as f:
            for k, v in image_builder_table.items():
                f.write('{},{},{}\n'.format(k, v['url'], ','.join(v['support'])))
    else:
        image_builder_table = {}
        with open('image_builder.csv') as f:
            for line in f:
                items = line.strip().split(',')
                image_builder_table[items[0]] = {'url':items[1], 'support':items[2:]}

    # in this loop, prepare the building directory for every firmware
    for k, v in image_builder_table.items():
        # TODO: confirm the way to get version
        openwrtver = v['url'].split('/')[4]
        supported_firmwares = "\n".join(v['support'])
        hash = k

        # 1. mkdir of this firmware (currently we use hash but each firmware a seperate building dir, we need to do this in the 1st round & then check which can be merged later)
        # name: openwrtversion-hash
        one_building_dir = '%s-%s' % (openwrtver, hash)
        try:
            os.mkdir("share/%s" % (one_building_dir))
        except OSError as exp:
            if exp.errno != errno.EEXIST:
                raise

        # 2. download the image_builder to ./share
        print(v['url'])
        os.system('wget -nc {} -P share'.format(v['url']))

        # 3. extract .config from the image builder(tar.bz2) to the building dir
        image_builder_name = os.path.basename(v['url']).replace('.tar.bz2', '')
        os.system('cd share && tar jxvf {0}.tar.bz2 {0}/.config && mv {0}/.config {1}/OpenWrt.config && rm -r {0}'.format(image_builder_name, one_building_dir))

        # 4. copy other things (patches to download.pl, makefiles, etc...)
        os.system('cp share/%s/* share/%s' % (openwrtver, one_building_dir))

        # 5. build the machine in the specified docker (manually)

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == '-s':
        build(search=True)
    elif len(sys.argv) == 1:
        build()
    else:
        print('usage {} [-s]'.format(sys.argv[0]))

