# OpenWRT Build Docker

Docker files for the OpenWRT Project.

+ docker volume `-v path/to/openwrt-build-docker/share:/root/firmware`

## Install

```bash
# Install `docker` if you don't have.
apt-get install -y docker.io && pip install docker-compose==1.19.0 && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose

# Install `python3.7` if you don't have.
add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt install -y python3.7 && \
    apt install -y python3-pip && python3.7 -m pip install --upgrade pip

# Install `virtualenv` if you don't have.
pip3.7 install virtualenv

# Install pyquery in virtual python environment.
mkdir -p ./pyenv
virtualenv -p `which python3.7` ./pyenv
source pyenv/bin/activate
pip install pyquery

# Download all the tar.gz files from this
[link](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck?usp=sharing)
and put them in `path/to/openwrt-build-docker/pre_download` folder.
```

## Summary
```
# csv
 0    1    2      3        4              5
uuid,hash,url,homepage,build_at,vmlinux_debug_info,
     6         7        8         9    10  11
source_code,vmlinux,dot_config,makeout,gcc,bin
```
