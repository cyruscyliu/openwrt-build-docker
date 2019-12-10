#!/usr/bin/python
import os
import sys

def search(uuid):
    # maybe we don't support this firmware
    uuids = {}
    with open('machines.csv') as f:
        for line in f:
            uuid_supported, url = line.strip().split(',')
            uuids[uuid_supported] = url
    if uuid not in uuids:
        print('add this new firmware to machines.csv')
        exit(-1)


    # find its hash
    hash_of_image_builder, candidates = None, None
    url = uuids[uuid]
    print('{}\tdownload from\t{}'.format(uuid, url))
    openwrtver = url.split('/')[4]
    homepage = os.path.dirname(url)
    print('{}\thomepage is\t{}'.format(uuid, homepage))
    with open('image_builder.csv') as f:
        for line in f:
            items = line.strip().split(',')
            hash_of_image_builder = items[0]
            url_to_image_builder = items[1]
            candidates = items[2:]
            hp = os.path.dirname(url_to_image_builder)
            if hp == homepage:
                break
    candidates.remove(uuid)
    print('{}\ttogether with\t{}'.format(uuid, candidates))
    if hash_of_image_builder is None:
        print('add this new firmware to machines.csv')
        exit(-1)

    print('{}\tbuild at\tshare/{}-{}'.format(uuid, openwrtver, hash_of_image_builder))

    # find path to vmlinux and path to source code
    # TODO





if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('usage {} UUID'.format(sys.argv[0]))
        exit(-1)
    search(sys.argv[1])
