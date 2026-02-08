#!/bin/sh

set -eu

PORT=/dev/ttyUSB0

mpremote connect $PORT fs cp src/main.py :main.py
mpremote connect $PORT fs cp src/boot.py :boot.py
mpremote connect $PORT reset

