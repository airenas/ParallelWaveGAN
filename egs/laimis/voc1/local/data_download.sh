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
    cd "${download_dir}"
    tar -vxf "${corpus_file}"
    mkdir -p "${corpus}/wavs"
    cd "WAV96CHUNK"
    for f in *$'\223'*.wav; do
        base="${f##*$'\223'}"
        # mv "$f" "../${corpus}/wavs/$base"
        ffmpeg -i "$f" -ar 22050 -ac 1 -sample_fmt s16 "../${corpus}/wavs/$base"
        rm "$f"
    done
    sed 's/^[^|]*–//' ARN_transcripts.txt | sort > ../${corpus}/metadata.csv
    echo "successfully prepared data."
    cd "${cwd}"
    echo "successfully prepared data."
else
    echo "already exists. skipped."
fi
