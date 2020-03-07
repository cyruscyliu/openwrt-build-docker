#!/bin/bash

if [[ "$(docker images -q openwrt-17.01:latest 2> /dev/null)" == "" ]]; then
  # do something
  docker build . -t openwrt-17.01:latest
fi