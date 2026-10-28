#!/bin/bash
cd /home/claude/research/w3_formats/code
rm -f ../out/lat_p16_m8.dump
exec /home/claude/research/bin/heavy 1750 bash -c "./latenum 10 word 1010101010101010 8 -nocone -dump ../out/lat_p16_m8.dump > ../out/uLAT8_p16_m8.txt 2>&1"
