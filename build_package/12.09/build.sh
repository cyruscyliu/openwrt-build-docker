#!/bin/bash

#
# config part
#
DOWNLOAD_URL="https://github.com/openwrt/archive/archive/v12.09.tar.gz"
PACKAGE_NAME="v12.09.tar.gz"
PACKAGE_DIR_NAME="archive-12.09"
CACHE_DL_TAR="12.09.dl.tar.gz"

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
 
rm -rf $PACKAGE_DIR_NAME && tar -xf $STORING_DIR/$PACKAGE_NAME

#
# patch and config
#
target=$PACKAGE_DIR_NAME
cp download.pl $target/scripts/download.pl
cp OpenWrt.config $target/.config
cp kernel-defaults.mk $target/include/kernel-defaults.mk
cp kernel-config-extra $target/kernel-config-extra
cp generic.mk $target/target/linux/orion/image/generic.mk
cp Makefile $target/target/linux/ramips/image/Makefile
cp 12.09-tools-upslug2-Makefile $target/tools/upslug2/Makefile

# feed dependency
if [ -f "$CACHE_DIR/$CACHE_DL_TAR" ]
then
    echo "using cached download file to accelerate"
    tar -xzf $CACHE_DIR/$CACHE_DL_TAR -C $PACKAGE_DIR_NAME
fi

# If not use the dl provided by us, you should additionally download the following 2 packages.
# And put them into the $target/dl
#http://mirror2.openwrt.org/sources/opkg-618.tar.gz
#http://mirror2.openwrt.org/sources/hotplug2-201.tar.gz

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
