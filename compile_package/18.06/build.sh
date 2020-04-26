#!/bin/bash

if [[ "$(docker images -q openwrt-18.06:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-18.06:latest
fi