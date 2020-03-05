# download the package
DOWNLOAD_URL="https://github.com/openwrt/openwrt/archive/v18.06.4.tar.gz"
PACKAGE_NAME="v18.06.4.tar.gz"
PACKAGE_DIR_NAME="openwrt-18.06.4"

export STORING_DIR=/root/firmware
echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- || true
rm -rf $PACKAGE_DIR_NAME && tar -xf $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"

tar -xzf $STORING_DIR/18.06.dl.tar.gz -C $PACKAGE_DIR_NAME

echo "building, logging at $PACKAGE_DIR_NAME/buildout.txt, please wait ..."

cd $PACKAGE_DIR_NAME || true
make -j16 V=s >buildout.txt 2>&1