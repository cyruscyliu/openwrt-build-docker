# openwrt-build-docker

Docker files for OpenWRT building envs.

+ for docker, the volume option should be `-v path/to/openwrt-build-docker/share:/root/firmware`
+ for the first time, check [dependency](#dependency) and [flow](#flow)

## Usage


## Summary
```
# csv
 0    1    2      3        4              5             6         7        8         9    10  11
uuid,hash,url,homepage,build_at,vmlinux_debug_info,source_code,vmlinux,dot_config,makeout,gcc,bin
```

### dependency

0. Install `docker` if you don't have.
```bash
apt-get install -y docker.io && pip install docker-compose==1.19.0 && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

1. Install `python3.7` if you don't have.
```bash
add-apt-repository ppa:deadsnakes/ppa && apt-get update && apt install -y python3.7 && \
    apt install -y python3-pip && python3.7 -m pip install --upgrade pip
```

2. Install `virtualenv` if you don't have.
```bash
pip3.7 install virtualenv
```

3. Install pyquery in virtual python environment.
```bash
mkdir -p ./pyenv
virtualenv -p `which python3.7` ./pyenv
source pyenv/bin/activate
pip install pyquery
```

### acceleration

Download all the tar.gz files from this [link](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck?usp=sharing) and put them in `path-to-this-repo/pre_download` folder.

These tar.gz will be unzipped and used in the build process, they accelerate the build by skipping the network downloading time.

Currently, we have tars for:

- 10.03
- 12.09
- 14.07
- 15.05.1
- 17.01.0-rc2
- 17.01.7
- 18.06.7
- 19.07.1