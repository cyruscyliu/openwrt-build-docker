#!/bin/bash

#
# config part
#
DOWNLOAD_URL="https://github.com/openwrt/openwrt/archive/v17.01.0-rc1.tar.gz"
PACKAGE_NAME="v17.01.0-rc1.tar.gz"
PACKAGE_DIR_NAME="openwrt-17.01.0-rc1"
CACHE_DL_TAR="17.01.dl.tar.gz"

#
# global const
#
STORING_DIR=/root/firmware
CACHE_DIR=/root/firmware/cache
NPROC=`nproc --all`

echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~-
rm -rf $PACKAGE_DIR_NAME && tar -xf $STORING_DIR/$PACKAGE_NAME

#
# patch and config
#
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"
cp "010-automake-port-to-Perl-5.22-and-later.patch" "$target/tools/automake/patches"
cp "005-misc-rename-copy_file_range-to-copy_file_chunk.patch" "$target/tools/e2fsprogs/patches"
cp "200-fix-zero-as-null.patch" "$target/toolchain/gdb/patches"
cp "image-commands.mk" "$target/include/image-commands.mk"

if [ -f "$CACHE_DIR/$CACHE_DL_TAR" ]
then
    echo "using cached download file to accelerate"
    tar -xzf $CACHE_DIR/$CACHE_DL_TAR -C $PACKAGE_DIR_NAME
fi

echo "building, logging at $PACKAGE_DIR_NAME/buildout.txt, please wait ..."

cd $PACKAGE_DIR_NAME

rm -f ../BUILD_ERROR
make -j${NPROC} V=s >buildout.txt 2>&1
ERR=$?
if [ "${ERR}" -ne 0 ]
then
    echo "Build error for the target.subtarget " "${ERR}" > ../BUILD_ERROR
    exit ${ERR}
fi