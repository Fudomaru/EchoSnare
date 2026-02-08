#!/bin/sh
set -eu

PORT=/dev/ttyUSB0
DST=scans_extracted

mkdir -p "$DST"

mpremote connect "$PORT" fs ls :/scans | tail -n +2 | while read -r _ f; do
    echo "Copying '$f'"
    mpremote connect "$PORT" fs cp ":/scans/$f" "$DST/$f"
done
