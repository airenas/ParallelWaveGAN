#!/bin/bash

# Copyright 2019 Tomoki Hayashi
#  MIT License (https://opensource.org/licenses/MIT)

download_dir=$1

# check arguments
if [ $# != 1 ]; then
    echo "Usage: $0 <download_dir>"
    exit 1
fi

set -euo pipefail

cwd=$(pwd)
if [ ! -e "${download_dir}/${corpus}" ]; then
    mkdir -p "${download_dir}"
    cp ${corpus_file} ${download_dir}/
    cd "${download_dir}"
    tar -vxf ./*.tar.gz
    rm ./*.tar.gz
    cd "${cwd}"
    echo "successfully prepared data."
else
    echo "already exists. skipped."
fi
