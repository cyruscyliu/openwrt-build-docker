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


def build():
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

    #print(image_builder_table)

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

    # 5. build the machine in the specified docker (maybe manually?)

    # 6. write all to support list
    # we need to locate the path:
    # the easiest way is to search the vmlinux.elf first,
    # then locate the linux source dir based on that


if __name__ == '__main__':
    build()
