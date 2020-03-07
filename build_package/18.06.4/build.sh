# download the package
DOWNLOAD_URL="https://github.com/openwrt/openwrt/archive/v18.06.4.tar.gz"
PACKAGE_NAME="v18.06.4.tar.gz"
PACKAGE_DIR_NAME="openwrt-18.06.4"

STORING_DIR=/root/firmware
CACHE_DIR=/root/firmware/cache
NPROC=`nproc --all`

echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- || true
rm -rf $PACKAGE_DIR_NAME && tar -xf $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"

#if [ -f "$CACHE_DIR/18.06.dl.tar.gz" ]
#then
#    echo "using cached download file to accelerate"
#    tar -xzf $CACHE_DIR/18.06.dl.tar.gz -C $PACKAGE_DIR_NAME
#fi

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