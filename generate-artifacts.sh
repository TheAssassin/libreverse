#! /bin/bash

set -e

log() {
    tput setaf 2
    echo "$*"
    tput sgr0
}

render_if_needed() {
    in_file="$1"
    out_file="$2"

    if [[ "$2" == "" ]]; then
        log "Usage: $0 <in_file> <out_file>"
        return 2
    fi

    if [[ ! -f "$in_file" ]]; then
        log "Error: $in_file does not exist"
        return 1
    fi

    if [[ -f "$out_file" ]] && [[ "$out_file" -nt "$in_file" ]]; then
        log "$out_file up to date, skipping generation"
        return 0
    fi

    log "Generating file $out_file"
    openscad -o "$out_file" "$in_file" --viewall
}

if [[ ! -d "$1" ]]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

find "$1" -type f -iname '*.scad' -print0 | while IFS= read -r -d '' in_file; do
    log "Generating data for $in_file"

    out_dir="$(dirname "$in_file")"

    basename="$(basename "$in_file" .scad)"

    png_file="$out_dir"/"$basename".png
    stl_file="$out_dir"/"$basename".stl

    render_if_needed "$in_file" "$png_file"
    render_if_needed "$in_file" "$stl_file"
done
