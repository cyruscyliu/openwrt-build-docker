# OpenWRT Build Docker

Docker files for the OpenWRT Project.
We support automatically building the OpenWrt project given a target/subtarget.

+ working directory out:in docker openwrt-build-docker/share:/root/firmware

## Install

```bash
apt-get install -y docker.io && pip install docker-compose==1.19.0 && \
    ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
pip install pyquery
```

## Usage

```
./openwrt defconfig/firmguide.batch -o firmguide.log

```

## Trouble shooting

+ If you want to handle building errors and rebuild manually, you need
  - go to the corresponding build directory
  - maybe modify `docker-compose.yml` and `build.sh` depending on what your need
  - run `./compile.sh`


## Currently supports

After testing all the 1400+ building configs, there are maybe 100-300 configs failed.
We follow the following rules to fix them.
- lowest priority, any other things for the research could preempt this
- lazy, we will fix the failing build that really stops us
- open, your contribution is very welcome and highly appreciated ;)

+ Table 1. the progress (supp/all) for all the latest versions for all target.subtarget.

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

+ Table 2. the progress (supp/all) for all the versions for all target.subtarget

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

+ Table 3. Detailed progress for every target.subtarget.

Please check [detailed-progress-table](./latest-process.md) 

## License

[MIT](./LICENSE)
