#!/bin/bash

set -x

script_dir=`dirname $0`

yml_temp=${script_dir}/docker-compose.tmp
build_dir=$1
predownload_dir=`realpath ${script_dir}/../../pre_download`

cd ${build_dir}
sed "s!BUILD_DIR!${build_dir}!g" ${yml_temp} | sed "s!CACHE_DIR!${predownload_dir}!g" > docker-compose.yml
COMPOSE_HTTP_TIMEOUT=120 docker-compose -f docker-compose.yml run firmware-build
COMPOSE_HTTP_TIMEOUT=120 docker-compose -f docker-compose.yml rm firmware-build