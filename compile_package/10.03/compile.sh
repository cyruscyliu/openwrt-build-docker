#!/bin/bash

script_dir=`dirname $0`

yml_path=${script_dir}/docker-compose.yml
build_dir=$1
predownload_dir=`realpath ${script_dir}/../../pre_download`

cd ${build_dir}
COMPOSE_HTTP_TIMEOUT=120 docker-compose -f ${yml_path} up -e BUILD_DIR=${build_dir} -e CACHE_DIR=${predownload_dir}