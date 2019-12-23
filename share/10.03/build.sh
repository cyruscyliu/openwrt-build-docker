# download the package
DOWNLOAD_URL="https://archive.openwrt.org/backfire/10.03/backfire_10.03_source.tar.bz2"
PACKAGE_NAME="backfire_10.03_source.tar.bz2"
PACKAGE_DIR_NAME="backfire_10.03"

export STORING_DIR=/root/firmware
echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- || true
rm -rf $PACKAGE_DIR_NAME && tar -jxf $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp download.pl $target/scripts/download.pl
cp Makefile $target/toolchain/binutils/Makefile
cp OpenWrt.config $target/.config
cp kernel-defaults.mk $target/include/kernel-defaults.mk
cp kernel-config-extra $target/kernel-config-extra

# feed dependency
tar -xzf $STORING_DIR/10.03.dl.tar.gz -C $PACKAGE_DIR_NAME

cd $PACKAGE_DIR_NAME || true
make -j16 >buildout.txt 2>&1
