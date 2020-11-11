#!/bin/bash

if [[ "$(docker images -q openwrt-15.05:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-15.05:latest
fi