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

## As Library
```python
from autobots_build import make_build_package, \
    make_compile_docker, do_the_building

target_dir = 'share'
openwrt_ver = '15.05'
config_path =  'path/to/image/builder/config' # =target+subtarget
tag = 'your_tag' # build_dir will be share/15.05-your_tag

compile_script = make_compile_docker(openwrt_ver)
build_dir = make_build_package(target_dir, openwrt_ver, config_path, tag=tag)
do_the_building(build_dir, compile_script)
```

## Reference
[autobots](https://github.com/occia/autobots), providing reusable APIs, DBs & knowledges based
on collected firmware kernel data, AST & LLVM IR.  
[docker-openwrt-buildroot](https://github.com/noonien/docker-openwrt-buildroot), a docker
container for the OpenWRT buildroot.
# Intro

Now support auto building the openwrt environment once given a subtarget or a firmware's uuid.
The firmware's uuid will be mapped to an (openwrt_ver, target, subtarget) tuple, and make the env according to this tuple.

# Dependency

Before run, you should:

- prepare `python 3.7` environment
- download [the pre download packages](https://drive.google.com/drive/folders/1KCdgytkYtWFmiXKlpb6nkqnoRGn9z9Ck) and put them into the `./pre_download` dir of the `openwrt-image-builder` when the tool reminds you to do that
- now you must have access to the `openwrt-image-builder` repo

# Usage

```
$ python setup_compile.py
Usage:
1. build env by uuid
setup_compile.py -u uuid [-o logfile] uuid1 uuid2 uuid3 ...

2. build env by subtarget
setup_compile.py [-u subtar] [-o logfile] openwrt_ver target subtarget
OR
setup_compile.py [-u subtar] [-o logfile] -l arglistfile


Options:
  -h, --help            show this help message and exit
  -u MODE, --unit=MODE  uuid or subtar, subtar is default
  -l LISTFILE, --list=LISTFILE
                        file contain ver tar subtar per line
  -o LOGFILE, --logout=LOGFILE
                        log file, by default the stdout

```

N.B.

- For the first time use, the tool will exit after pulling the repo `openwrt-image-build` and switching to the right branch. This is to remind you to download the pre download tar things
- For option `-o`, it will append to the log file you specified rather than truncate & rewrite
- If you want to handle building error and rebuild manually, you need the following flow
  - go to the corresponding build directory
  - maybe modify `docker-compose.yml` & `build.sh` depending on your need
  - run `bash re_compile.sh`


# Currently supports (outdated, pls directly see [detailed_progress.md](./detailed_progress.md))

After we tests all the 1400+ building configs, there should still left fails to build configs(maybe 100-300). We follow the following rules to fix them:
- lowest priority, any other things for the research could preempt this
- lazy, we will fix the failing build that really stops us
- open, your contribution is very welcome and highly appreciated ;)

Table 1. the progress (supp/all) for all the latest versions for all target.subtarget.

|      latest version     | latest | oldest | middle |  all  |
|:-----------------------:|:------:|:------:|:------:|:-----:|
|         19.07.1         | 53/56  | 0/0    |  0/0   | 53/56 |
|         18.06.7         | 8/9    | 0/0    | 44/46  | 52/55 |
|         17.01.7         | 10/10  | 0/0    |  -/35  | 10/45 |
|       17.01.0-rc2       | 7/8    | 0/0    |  -/47  | 7/55  |
|         15.05.1         | 3/4    | -/1    |  -/47  | 3/52  |
|          14.07          | -/11   | -/10   |  -/15  | -/36  |
|          12.09          | 7/10   | 11/16  |  6/10  | 24/36 |
|          10.03          | 3/3    | 14/14  |  0/0   | 17/17 |

Table 2. the progress (supp/all) for all the versions for all target.subtarget

|       version        | all (supp/all) |
|:--------------------:|:--------------:|
|  backfire_10.03      |      17/17     |
|  archive-12.09       |      24/36     |
|  archive-14.07       |      -/36      |
|  archive-15.05       |      -/51      |
|  archive-15.05.1     |      3/52      |
|  openwrt-17.01.0     |      -/45      |
|  openwrt-17.01.0-rc1 |      -/54      |
|  openwrt-17.01.0-rc2 |      7/55      |
|  openwrt-17.01.1     |      -/45      |
|  openwrt-17.01.2     |      -/44      |
|  openwrt-17.01.3     |      -/44      |
|  openwrt-17.01.4     |      -/45      |
|  openwrt-17.01.5     |      -/45      |
|  openwrt-17.01.6     |      -/45      |
|  openwrt-17.01.7     |      10/45     |
|  openwrt-18.06.0     |      -/54      |
|  openwrt-18.06.0-rc1 |      -/51      |
|  openwrt-18.06.0-rc2 |      -/52      |
|  openwrt-18.06.1     |      -/56      |
|  openwrt-18.06.2     |      -/55      |
|  openwrt-18.06.3     |      -/56      |
|  openwrt-18.06.4     |      -/56      |
|  openwrt-18.06.5     |      -/55      |
|  openwrt-18.06.6     |      -/55      |
|  openwrt-18.06.7     |      52/55     |
|  openwrt-19.07.0     |      -/56      |
|  openwrt-19.07.0-rc1 |      -/56      |
|  openwrt-19.07.0-rc2 |      -/56      |
|  openwrt-19.07.1     |      53/56     |
|      summary         |    166/1428    |

Table 3. Detailed progress for every target.subtarget, see [detailed-progress-table](./detailed_progress.md) 
