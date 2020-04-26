# OpenWRT Build Docker

Docker files for the OpenWRT Project.
+ supports 10.03 14.07 15.05.1 17.01.0-rc1 17.01.1 17.01.3 17.01.5 17.01.7 18.06.0-rc1
18.06.1 18.06.3 18.06.5 18.06.7 19.07.0-rc1 19.07.1 12.09 15.05 17.01.0 17.01.0-rc2
17.01.2 17.01.4 17.01.6 18.06.0 18.06.0-rc2 18.06.2 18.06.4 18.06.6 19.07.0 19.07.0-rc2
+ working directory out:in docker openwrt-build-docker/share:/root/firmware

## Install

```bash
apt-get install -y docker.io && pip install docker-compose==1.19.0 && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
pip install pyquery
```
Download all the tar.gz files from this
[link](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck?usp=sharing)
and put them in `path/to/openwrt-build-docker/pre_download` folder.

## Usage

You can select the OpenWRT revisions and targets you'd like to build by `-v` and `-t`.
Neither `-v` nor `-t` is selected, we'll build all revisions and all targets. If you
don't select `-rb`, then the real building process won't start, just for some simple tasks.
If you select `-uo`, then nothing except the `image_builder.cache` where you can check
where your build directories are will be updated.
```bash
./build -v 15.05 -t ramips -uo
```

## Reference
[autobots](https://github.com/occia/autobots), providing reusable APIs, DBs & knowledges based
on collected firmware kernel data, AST & LLVM IR.  
[docker-openwrt-buildroot](https://github.com/noonien/docker-openwrt-buildroot), a docker
container for the OpenWRT buildroot.

