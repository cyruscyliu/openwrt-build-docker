#!/bin/bash

if [[ "$(docker images -q openwrt-10.03:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-10.03:latest
fi