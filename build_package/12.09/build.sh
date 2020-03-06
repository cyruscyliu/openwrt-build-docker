# download the package
DOWNLOAD_URL="https://github.com/openwrt/archive/archive/v12.09.tar.gz"
PACKAGE_NAME="v12.09.tar.gz"
PACKAGE_DIR_NAME="archive-12.09"

export STORING_DIR=/root/firmware
echo "openwrt" | sudo -S chown -R openwrt:openwrt $PWD

cd $STORING_DIR && wget -nc $DOWNLOAD_URL && cd ~- || true
rm -rf $PACKAGE_DIR_NAME && tar -xf $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp download.pl $target/scripts/download.pl
cp OpenWrt.config $target/.config
cp kernel-defaults.mk $target/include/kernel-defaults.mk
cp kernel-config-extra $target/kernel-config-extra
cp generic.mk $target/target/linux/orion/image/generic.mk
cp Makefile $target/target/linux/ramips/image/Makefile

# feed dependency
tar -xf $STORING_DIR/12.09.dl.tar.gz -C $PACKAGE_DIR_NAME

# If not use the dl provided by us, you should additionally download the following 2 packages.
# And put them into the $target/dl
#http://mirror2.openwrt.org/sources/opkg-618.tar.gz
#http://mirror2.openwrt.org/sources/hotplug2-201.tar.gz

echo "building, logging at $PACKAGE_DIR_NAME/buildout.txt, please wait ..."

cd $PACKAGE_DIR_NAME
make -j16 V=s >buildout.txt 2>&1
