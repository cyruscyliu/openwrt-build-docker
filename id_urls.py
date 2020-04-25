#!/usr/bin/python
"""
Extract id,url from firmware repository.
"""
import os
import argparse


def generate_machine_id_url(path):
    header = None
    records = []

    with open(path) as f:
        for line in f:
            items = line.strip().split(',')
            if header is None:
                header = items
                continue
            records.append(items)
    machines = []
    for record in records:
        uuid = record[header.index('id')]
        url = record[header.index('url')]
        machines.append([uuid, url])

    with open('id_urls.csv', 'w') as f:
        f.write(','.join(['id', 'url']))
        f.write('\n')
        for machine in machines:
            f.write(','.join(machine))
            f.write('\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('repository', help='firmware repository which contains at least id,url columns')
    args = parser.parse_args()

    path = args.repository
    if not os.path.exists(path):
        print('{} doesn\'t exist'.format(path))
        exit(-1)
    generate_machine_id_url(path)

