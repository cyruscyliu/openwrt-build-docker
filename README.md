# OpenWRT Build Docker

Docker files for the OpenWRT Project.
+ supports 10.03 14.07 15.05.1 17.01.0-rc1 17.01.1 17.01.3 17.01.5 17.01.7 18.06.0-rc1
18.06.1 18.06.3 18.06.5 18.06.7 19.07.0-rc1 19.07.1 12.09 15.05 17.01.0 17.01.0-rc2
17.01.2 17.01.4 17.01.6 18.06.0 18.06.0-rc2 18.06.2 18.06.4 18.06.6 19.07.0 19.07.0-rc2
+ working directory out:in docker openwrt-build-docker/share:/root/firmware

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
```
Download all the tar.gz files from this
[link](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck?usp=sharing)
and put them in `path/to/openwrt-build-docker/pre_download` folder.

## Usage

You can select the OpenWRT revisions and targets you'd like to build by `-v` and `-t`.
Neither `-v` nor `-t` is selected, we'll build all revisions and all targets. If you
don't select `-rb`, then the real building process won't start, just for some simple tasks.
```bash
./build -v 15.05 -t ramips -rb
```

## Reference
[autobots](https://github.com/occia/autobots), providing reusable APIs, DBs & knowledges based
on collected firmware kernel data, AST & LLVM IR.
[docker-openwrt-buildroot](https://github.com/noonien/docker-openwrt-buildroot), a docker
container for the OpenWRT buildroot.

