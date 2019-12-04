# download the package
DOWNLOAD_URL="https://github.com/openwrt/chaos_calmer/archive/v15.05.zip"
PACKAGE_NAME="v15.05.zip"
PACKAGE_DIR_NAME="chaos_calmer-15.05"

export STORING_DIR=/root/firmware

echo "openwrt" | sudo -S chown -R openwrt:openwrt $STORING_DIR

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd - || true
rm -rf $PACKAGE_DIR_NAME && unzip $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp "OpenWrt.config" "$target/.config"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"

tar -xzvf $STORING_DIR/15.05.dl.tar.gz -C $PACKAGE_DIR_NAME

cd $PACKAGE_DIR_NAME || true
make -j4
