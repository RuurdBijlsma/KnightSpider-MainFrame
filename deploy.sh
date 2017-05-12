#!/usr/bin/env bash
echo "Copying files"

scp ./*.py pi@$1:/home/pi/Python/KnightSpider-MainFrame/
