#!/usr/bin/python
"""
Extract image url from firmware repository.
"""
import os
import argparse


def generate_image_url(path):
    header = None
    records = []

    with open(path) as f:
        for line in f:
            items = line.strip().split(',')
            if header is None:
                header = items
                continue
            records.append(items)
    urls = []
    for record in records:
        url = record[header.index('url')]
        urls.append(url)

    with open('image_builder.url', 'w') as f:
        f.write('url\n')
        for url in urls:
            f.write('{}\n'.format(url))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('repository', help='firmware repository which contains at least a url column')
    args = parser.parse_args()

    path = args.repository
    if not os.path.exists(path):
        print('{} doesn\'t exist'.format(path))
        exit(-1)
    generate_image_url(path)

