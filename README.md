# openwrt-build-docker

Docker files for OpenWRT building envs.

## dependency

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

## acceleration


Put them in `share`.

+ [10.03.dl.tar.gz](https://drive.google.com/file/d/1S4TdLBQDgnVv2cifXMhSR1umo5_Bo2tu/view?usp=sharing)
+ [12.09.dl.tar.gz](https://drive.google.com/open?id=1hc0PujRBhNEn_2zC8_etlGmVJAYHEq6Q)
+ [15.05.dl.tar.gz](https://drive.google.com/file/d/1R86VpMVnaCLeb_iHCRAqkV_sSTc40-i-/view?usp=sharing)


## quick start

Take OpenWRT 10.03 as an example.

```shell script
cd 10.03
./build.sh # build the docker image locally
./start.sh # run the docker daemon
./in.sh # get the shell, enter exit to exit
# now we are in the docker, choose one machine
cd 10.03-openwrt350_nv2 && build.sh
# ./remove.sh  # remove the docker daemon
```
## automation

Given the offical url where you download your firmware and a uuid for the firmware, we can generate the building files
w.s.t to this firmware and find its vmlinux and source code directory automatically. See [build.py](./build.py) for details.

```shell script
./build
# manully build
./build -s # update support list
```

Using the uuid you can get the path to its vmlinux and path to the source code, just type `search.py UUID`.

```shell script
./search 14235
14235   download from   http://archive.openwrt.org/chaos_calmer/15.05/brcm47xx/mips74k/openwrt-15.05-brcm47xx-mips74k-asus-rt-n10u-squashfs.trx
14235   homepage is http://archive.openwrt.org/chaos_calmer/15.05/brcm47xx/mips74k
14235   together with   []
14235   build at    share/15.05-c771ee4bc428900c59114713e76e54f6
14235   source code share/15.05-c771ee4bc428900c59114713e76e54f6/./chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/linux-3.18.20
14235   vmlinux.elf share/15.05-c771ee4bc428900c59114713e76e54f6/./chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/linux-3.18.20/vmlinux
14235   with symbol share/15.05-c771ee4bc428900c59114713e76e54f6/./chaos_calmer-15.05/bui  ld_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/vmlinux.elf-debug-info
14235   and .config share/15.05-c771ee4bc428900c59114713e76e54f6/./chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/linux-3.18.20/.config
```

## support list

[support_list.csv](./support_list.csv)

## stats
||10.03|12.09|15.05|sum|
|:---:|:---:|:---:|:---:|:---:|
|firmware we have|16|22|37|75|
|distinct homepage|7|6|9|22|
|souce code we support|7|4|9|20|

## problems in manully building

+ set KGDB_XXX flags =n
+ [vmlinux-all0239-3g.bin.lzma.combined: No such file or directory](https://forum.archive.openwrt.org/viewtopic.php?id=41831)
