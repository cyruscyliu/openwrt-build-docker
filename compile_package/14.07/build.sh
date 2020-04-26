#!/bin/bash

if [[ "$(docker images -q openwrt-14.07:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-14.07:latest
fi