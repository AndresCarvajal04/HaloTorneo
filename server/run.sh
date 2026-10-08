#!/bin/bash

# Force 32-bit Wine prefix
export WINEARCH=win32
export WINEPREFIX=/home/haloadmin/.wine

# Set server port
PORT=2302

# Get the script directory
ROOT="$(dirname "$(realpath "$0")")"
cd "$ROOT"

# Set paths
CG_PATH="$ROOT/cg"
INIT_FILE="$CG_PATH/init.txt"

# Launch Server
wine "$ROOT/haloceded.exe" -path "$CG_PATH" -exec "$INIT_FILE" -port $PORT
