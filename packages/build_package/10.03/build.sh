#!/bin/bash

#
# config part
#
DOWNLOAD_URL="https://archive.openwrt.org/backfire/10.03/backfire_10.03_source.tar.bz2"
PACKAGE_NAME="backfire_10.03_source.tar.bz2"
PACKAGE_DIR_NAME="backfire_10.03"
CACHE_DL_TAR="10.03.dl.tar.gz"

#
# global const
#
STORING_DIR=/root/firmware
CACHE_DIR=/root/firmware/cache
NPROC=`nproc --all`

echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

if [ -f "$CACHE_DIR/$PACKAGE_NAME" ]
then
    echo "using cached download source to accelerate"
    cp "$CACHE_DIR/$PACKAGE_NAME" $STORING_DIR/
else
    cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- 
fi

rm -rf $PACKAGE_DIR_NAME && tar -jxf $STORING_DIR/$PACKAGE_NAME

#
# patch and config
#
target=$PACKAGE_DIR_NAME
cp download.pl $target/scripts/download.pl
cp Makefile $target/toolchain/binutils/Makefile
cp OpenWrt.config $target/.config
cp kernel-defaults.mk $target/include/kernel-defaults.mk
cp kernel-config-extra $target/kernel-config-extra

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