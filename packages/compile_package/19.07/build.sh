#!/bin/bash

if [[ "$(docker images -q openwrt-19.07:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-19.07:latest
fi