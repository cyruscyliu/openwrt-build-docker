#!/usr/bin/python

import os

TARGET_VERSIONS = ['10.03', '12.09', '15.05']

stats = {}
with open('image.builder.csv') as f:
    for line in f:
        things = line.strip().split(',')
        u = things[1]
        ids = things[3:]
        for target_version in TARGET_VERSIONS:
            if line.find(target_version) != -1:
                if target_version in stats:
                    stats[target_version]['count'] += 1
                else:
                    stats[target_version] = {'count':1, 'firmware':0}
                stats[target_version]['firmware'] += len(ids)
print(stats)
