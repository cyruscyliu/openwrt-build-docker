# openwrt-build-docker

Docker files for OpenWRT building envs refer to [firmware-uuid](https://github.com/cyruscyliu/firmware-uuid).

+ for docker, the volume option should be `-v path/to/openwrt-build-docker/share:/root/firmware`
+ for the first time, check [dependency](#dependency) and [flow](#flow)

## statistics
{'15.05': {'count': 26, 'firmware': 812}, '10.03': {'count': 10, 'firmware': 137}, '12.09': {'count': 18, 'firmware': 518}}

||10.03|12.09|15.05|sum|
|:---:|:---:|:---:|:---:|:---:|
|distinct targets|10|18|26|54|
|firmware blob|137|518|812|1467|

## automation

Using [firmware-uuid](https://github.com/cyruscyliu/firmware-uuid), we known the uuid for a firmware and the url 
where you can download it. We can generate the building files w.s.t to this firmware and find its vmlinux and
source code directory automatically. See [build](./build.py) for details.

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

+ at last, summary all we have done
```
./build -s
```

## summary
```
# csv
 0    1    2      3        4              5             6         7        8         9    10  11
uuid,hash,url,homepage,build_at,vmlinux_debug_info,source_code,vmlinux,dot_config,makeout,gcc,bin
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