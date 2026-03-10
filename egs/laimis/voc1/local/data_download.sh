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
if [ ! -e "${download_dir}/corpus/.done" ]; then
    mkdir -p "${download_dir}/corpus"
    unzip "$corpus_file" -d ${download_dir}/corpus
    for f in "${download_dir}/corpus/wavs/*.wav"; do
        base=$(basename "$f")
        ffmpeg -i "$f" -ar 22050 -ac 1 -sample_fmt s16 "wavs16/$base" && rm "$f"
    done
    echo "successfully extracted data."
    touch "${download_dir}/corpus/.done"
else
    echo "already exists. skipped."
fi
