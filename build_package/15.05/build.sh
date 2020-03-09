#!/bin/bash

#
# config part
#
DOWNLOAD_URL="https://github.com/openwrt/archive/archive/v15.05.tar.gz"
PACKAGE_NAME="v15.05.tar.gz"
PACKAGE_DIR_NAME="archive-15.05"
CACHE_DL_TAR="15.05.dl.tar.gz"

#
# global const
#
STORING_DIR=/root/firmware
CACHE_DIR=/root/firmware/cache
NPROC=`nproc --all`

echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~-
rm -rf $PACKAGE_DIR_NAME && tar xf $STORING_DIR/$PACKAGE_NAME >/dev/null 2>&1

#
# patch and config
#
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"
cp "Makefile" "$target/target/linux/ar71xx/image/Makefile"

if [ -f "$CACHE_DIR/$CACHE_DL_TAR" ]
then
    echo "using cached download file to accelerate"
    tar -xzf $CACHE_DIR/$CACHE_DL_TAR -C $PACKAGE_DIR_NAME
fi

echo "building, logging at $PACKAGE_DIR_NAME/buildout.txt, please wait ..."

cd $PACKAGE_DIR_NAME

touch ../BUILD_ERROR
make -j${NPROC} V=s >buildout.txt 2>&1
ERR=$?
if [ "${ERR}" -ne 0 ]
then
    # second check without parallel
    make -j1 V=s >buildout.txt 2>&1
    ERR=$?
    if [ "${ERR}" -ne 0 ]
    then
        echo "Build error for the target.subtarget " "${ERR}" > ../BUILD_ERROR
        exit ${ERR}
    fi
fi
rm -f ../BUILD_ERROR