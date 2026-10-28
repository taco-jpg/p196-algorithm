#!/bin/bash
cd /home/claude/research/w2_theory/own/bin
echo "=== positive control base 2"; timeout 100 ./a113_regular 2 1010 1010 0001 --depth 8 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 90 2>&1 | tail -12
echo "=== positive control base 4"; timeout 100 ./a113_regular 4 100100 100100 000001 --depth 8 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 90 2>&1 | tail -8
echo "=== p11 engine"; timeout 300 ./a113_regular 10 10100110011 11100010000 01000010000 --depth 8 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 280 2>&1 | tail -15
echo "=== p11 engine | checker"; set -o pipefail
timeout 600 ./a113_regular 10 10100110011 11100010000 01000010000 --text-depth 5 --depth 5 --states 1000000 --edges 20000000 --ops 1000000000 --seconds 300 | ./a113_check - --seconds 280 --memory-mib 2048 --states 5000000 --ops 600000000 2>&1 | tail -30
