#!/usr/bin/python
"""
We are going to build machines in machines.csv.
"""
import os
import sys
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


def build():
    header = None
    # we found a .config always in an ImageBuilder
    # we also found many firmware share the same ImageBuilder
    # because they are downloaded from the same page
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
            hash_of_image_builder = hash(url_to_image_builder)
            if hash_of_image_builder in image_builder_table:
                image_builder_table[hash(url_to_image_builder)]['support'].append(uuid)
            else:
                image_builder_table[hash(url_to_image_builder)] = {'url': url_to_image_builder, 'support': [uuid]}
    # save image_builder_table
    with open('image_builder.txt', 'w') as f:
        for k, v in image_builder_table.items():
            f.write('{},{},{}\n'.format(k, v['url'], ','.join(v['support'])))
    # download the image_builder to share
    for k, v in image_builder_table.items():
        os.system('wget -nc {} -P share'.format(v['url']))
        # TODO
        # get .config
        # build this machine
        # write to support list


if __name__ == '__main__':
    build()
