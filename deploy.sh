#!/bin/sh

set -eu

PORT=/dev/ttyUSB0

echo "[*] Deploying all src/ files to ESP32..."

mpremote connect "$PORT" fs cp -r src/* :

echo "[✓] Deployment complete."
