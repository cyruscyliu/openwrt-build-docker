#!/usr/bin/python

"""
We are going to find
    1. source code
    2. vmlinux with debug info
    by given firmware uuid.
"""
import os
import sys


def get_openwrt_source_code(uuid):
    with open('image_builder.csv') as f:
        for line in f:
            items = line.strip().split(',')
            target_machine = {'hash': items[0], 'url': items[1], 'support': items[2:]}
            if uuid in items[2:]:
                break
    hash_to_machine = str(target_machine['hash'])
    path_to_vmlinux, path_to_source_code = None, None
    with open('support_list.csv') as f:
        for line in f:
            if line.startswith(hash_to_machine):
                print(line)

                path_to_vmlinux = line.strip().split(',')[1]
                path_to_source_code = line.strip().split(',')[2]
    return path_to_source_code, path_to_vmlinux


if __name__ == '__main__':
    print(get_openwrt_source_code('15007'))
