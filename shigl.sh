#!/bin/bash
# shigl.sh - اجرا کننده SHIGL

if [ -z "$1" ]; then
    echo "Usage: ./shigl.sh <file.shigl>"
    exit 1
fi

if [ ! -f "$1" ]; then
    echo "File not found: $1"
    exit 1
fi

python3 shigl_cli.py "$1"