# openwrt-build-docker

Docker files for OpenWRT building envs.

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

## support list

|openwrt|machine|status|vmlinux.elf|gdb working dir|
|:---:|:---:|:---:|:--:|:--:|
|10.03|openwrt350_nv2|Y|share/10.03-openwrt350_nv2/backfire_10.03/build_dir/linux-orion_generic/vmlinux.elf-debug-info|share/10.03-openwrt350_nv2/backfire_10.03/build_dir/linux-orion_generic/linux-2.6.32.10/|
|10.03|wr703n_v1|Y|share/12.09-wr703n-v1/archive-12.09/build_dir/linux-ar71xx_generic/vmlinux.elf-debug-info|share/12.09-wr703n-v1/archive-12.09/build_dir/linux-ar71xx_generic/linux-3.3.8/|
|15.05|nas7820|Y|share/15.05-nas7820/chaos_calmer-15.05/build_dir/target-arm_mpcore_uClibc-0.9.33.2_eabi/linux-oxnas/vmlinux.elf-debug-info|share/15.05-nas7820/chaos_calmer-15.05/build_dir/target-arm_mpcore_uClibc-0.9.33.2_eabi/linux-oxnas/linux-3.18.20/|
|15.05|wrt320n_nv1|Y|share/15.05-wrt320_nv1/chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/vmlinux.elf-debug-info|share/15.05-wrt320_nv1/chaos_calmer-15.05/build_dir/target-mipsel_74kc+dsp2_uClibc-0.9.33.2/linux-brcm47xx_mips74k/linux-3.18.20/|
