if [[ "$(docker images -q openwrt-12.09:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-12.09:latest
fi