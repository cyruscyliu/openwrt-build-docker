# openwrt-build-docker

Docker files for OpenWRT building envs.

## dependency

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

Using the uuid you can get the path to its vmlinux and path to the source code, just type `search.py UUID`.

## support list

|openwrt|machine|status|vmlinux.elf|gdb working dir|
|:---:|:---:|:---:|:--:|:--:|
|10.03|openwrt350_nv2|Y|share/10.03-openwrt350_nv2/backfire_10.03/build_dir/linux-orion_generic/vmlinux.elf-debug-info|share/10.03-openwrt350_nv2/backfire_10.03/build_dir/toolchain-arm_v5t_gcc-4.3.3+cs_uClibc-0.9.30.1_eabi/linux/|
|12.09|wr703n_v1|Y|share/12.09-wr703n-v1/archive-12.09/build_dir/linux-ar71xx_generic/vmlinux.elf-debug-info|share/12.09-wr703n-v1/archive-12.09/build_dir/linux-ar71xx_generic/linux-3.3.8/|
|15.05|nas7820|Y|share/15.05-nas7820/chaos_calmer-15.05/build_dir/target-arm_mpcore_uClibc-0.9.33.2_eabi/linux-oxnas/vmlinux.elf-debug-info|share/15.05-nas7820/chaos_calmer-15.05/build_dir/toolchain-arm_mpcore_gcc-4.8-linaro_uClibc-0.9.33.2_eabi/linux-3.18.20/|
|15.05|wrt320n_nv1|Y|share/15.05-wrt320_nv1/chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/vmlinux.elf-debug-info|share/15.05-wrt320_nv1/chaos_calmer-15.05/build_dir/toolchain-mipsel_74kc+dsp2_gcc-4.8-linaro_uClibc-0.9.33.2/linux-3.18.20/|
