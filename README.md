# openwrt-build-docker

Docker files for OpenWRT building envs.

## acceleration

Put them in `share`.

+ [10.03.dl.tar.gz](https://drive.google.com/file/d/1S4TdLBQDgnVv2cifXMhSR1umo5_Bo2tu/view?usp=sharing)


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

## machine supported

|openwrt|machine|status|
|:---:|:---:|:---:|
|10.03|openwrt350_nv2|Y|
|15.05|nas7820|Y|
|15.05|wrt320n_nv1|N|



