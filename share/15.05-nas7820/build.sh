# download the package
DOWNLOAD_URL="https://github.com/openwrt/chaos_calmer/archive/v15.05.zip"
PACKAGE_NAME="v15.05.zip"
PACKAGE_DIR_NAME="chaos_calmer-15.05"

export STORING_DIR=/root/firmware

cd $STORING_DIR && wget -N $DOWNLOAD_URL && cd - || true
rm -rf $PACKAGE_DIR_NAME && unzip $STORING_DIR/$PACKAGE_NAME

# patch and config
target=$PACKAGE_DIR_NAME
cp ".config" "$target/.config"
cp "download.pl" "$target/scripts/download.pl"
cp "libjson-c.makefile" "$target/package/libs/libjson-c/Makefile"
cp "ipset-dns.makefile" "$target/package/network/services/ipset-dns/Makefile"
cp "openvpn.makefile" "$target/package/network/services/openvpn/Makefile"
cp "xfsprogs.makefile" "$target/package/utils/xfsprogs/Makefile"
cp "kernel-defaults.mk" "$target/include/kernel-defaults.mk"
cp "kernel-config-extra" "$target/kernel-config-extra"

cd $PACKAGE_DIR_NAME || true
make -j4
