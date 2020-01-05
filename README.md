# openwrt-build-docker

Docker files for OpenWRT building envs.

+ for [llbic](https://github.com/cyruscyliu/llbic), the volume option should be 
`-v path/to/openwrt-build-docker/share:/root/firmware`
+ for the first time, check [dependency](#dependency) and [flow](#flow)

## statistics

[support_list.csv](./support_list.csv)

||10.03|12.09|15.05|sum|
|:---:|:---:|:---:|:---:|:---:|
|firmware we have|16|22|37|75|
|distinct homepages|7|6|9|22|
|souce code we support|7|6|9|22|

## automation

Given the offical url where you download your firmware and a uuid for the firmware, we can generate the building files
w.s.t to this firmware and find its vmlinux and source code directory automatically. See [build](./build.py) for details.

+ suppose I download the firmware http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin and assign it a uuid 14883
```
# machines.csv
14883,http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin
```

+ then run `./build` to generate patches and commands
```
share/15.05-cc3a47a374475253f93a08eea6eaadce/
|-- OpenWrt.config # patch
|-- build.sh # commands
|-- kernel-config-extra # patch
`-- kernel-defaults.mk # patch
```

let's see what's in ./share/15.05-cc3a47a374475253f93a08eea6eaadce/build.sh
```
# download the package
DOWNLOAD_URL="https://github.com/openwrt/chaos_calmer/archive/v15.05.zip"
PACKAGE_NAME="v15.05.zip"
PACKAGE_DIR_NAME="chaos_calmer-15.05"

export STORING_DIR=/root/firmware
echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- || true
rm -rf $PACKAGE_DIR_NAME && unzip $STORING_DIR/$PACKAGE_NAME >/dev/null 2>&1

# patch and config
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"

tar -xzf $STORING_DIR/15.05.dl.tar.gz -C $PACKAGE_DIR_NAME

cd $PACKAGE_DIR_NAME || true
make -j16 V=s >buildout.txt 2>&1
```

+ build your project
```
cd 10.03 && ./in.sh
cd 15.05-cc3a47a374475253f93a08eea6eaadce && ./build.sh
exit
```

+ at last, update `support_list.esv`
```
./build -s
```

## query

Using the uuid you can get the path to its vmlinux and path to the source code, just type `search UUID`.
Firmware sensitive information is not in `support_list.esv`, so use `search -s UUID` to generate a summary as interface.

```shell script
# search 14883
14883	download from	http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin
14883	homepage is	http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic
14883	together with	['14550', '14759', '14567', '14545', '14744', '14591', '14693', '14745', '14855', '14848', '14764', '14876', '14867']
14883	build at	share/15.05-cc3a47a374475253f93a08eea6eaadce
14883	source code	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20
14883	vmlinux.elf	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20/vmlinux
14883	with symbols	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/vmlinux.elf-debug-info
14883	and .config	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20/.config
14883	and makeout.txt	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/makeout.txt
14883	gcc	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/OpenWrt-SDK-15.05-ar71xx-generic_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64/staging_dir/toolchain-mips_34kc_gcc-4.8-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gcc
14883	firmware	share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/bin/ar71xx/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin

# sesarch -s 14883
14883,http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin,http://archive.openwrt.org/chaos_calmer/15.05/ar71xx/generic,14550@14759@14567@14545@14744@14591@14693@14745@14855@14848@14764@14876@14867,share/15.05-cc3a47a374475253f93a08eea6eaadce,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20/vmlinux,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/vmlinux.elf-debug-info,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/linux-3.18.20/.config,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/linux-ar71xx_generic/makeout.txt,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/build_dir/target-mips_34kc_uClibc-0.9.33.2/OpenWrt-SDK-15.05-ar71xx-generic_gcc-4.8-linaro_uClibc-0.9.33.2.Linux-x86_64/staging_dir/toolchain-mips_34kc_gcc-4.8-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-gcc,share/15.05-cc3a47a374475253f93a08eea6eaadce/./chaos_calmer-15.05/bin/ar71xx/openwrt-15.05-ar71xx-generic-ubnt-rs-squashfs-sysupgrade.bin
```

## license
[MIT](./LICENSE)

## appendix

### flow

Take OpenWRT 10.03 as an example. Suppose you are building a firmware of OpenWRT 10.03.
You are firstly expected to enter the OpenWRT 10.03 docker environment. 
Then, go to your openwrt project, patch and build it. The reason why you have to patch
the openwrt project is some source mirrors are invalid and some packages are changed causing mismatch hash.
We recommend you using packages (see [acceleration](#acceleration)) to smooth you building. It's annoying
to downloading openwrt source code, to wait for errors such that you know where to patch, etc., 
so we provide you with an [automated solution](#automation).

```shell script
# download openwrt-build-docker
git clone https://github.com/cyruscyliu/openwrt-build-docker.git && cd openwrt-build-docker

# prepare OpenWRT docker envirotment
cd 10.03 && ./build.sh # build the docker image locally
./start.sh && ./in.sh # run the docker daemon and get its shell

# choose one project, patch your project, and build (all projects should be put in `share` folder)

exit && ./remove.sh  # exit and remove the docker daemon
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

Put them in `share` folder.

+ [10.03.dl.tar.gz](https://drive.google.com/file/d/1S4TdLBQDgnVv2cifXMhSR1umo5_Bo2tu/view?usp=sharing)
+ [12.09.dl.tar.gz](https://drive.google.com/open?id=1hc0PujRBhNEn_2zC8_etlGmVJAYHEq6Q)
+ [15.05.dl.tar.gz](https://drive.google.com/file/d/1R86VpMVnaCLeb_iHCRAqkV_sSTc40-i-/view?usp=sharing)
