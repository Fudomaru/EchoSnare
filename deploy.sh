#!/bin/sh

set -eu

PORT=/dev/ttyUSB0

echo "[*] Deploying all src/ files to ESP32..."

mpremote connect "$PORT" fs cp -r src/* :

echo "[*] Resetting device..."
mpremote connect "$PORT" reset

echo "[✓] Deployment complete."
