#!/bin/bash

script_dir=`dirname $0`
yml_path=${script_dir}/docker-compose.yml
build_dir=$1

cd ${build_dir}
COMPOSE_HTTP_TIMEOUT=120 docker-compose -f ${yml_path} up -e BUILD_DIR=${build_dir}