#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -O3 -std=c++17 replay.cpp -lgmp -o /tmp/p196_n16_gmp
g++ -O3 -std=c++17 independent.cpp -o /tmp/p196_n16_digits
for test in '100 2000 39a381b57f874fdc' '300 20000 56371448fdcc1993' '301 20000 38532804c84fb2e8'; do
 set -- $test
 a=$(/tmp/p196_n16_gmp "$1" "$2")
 b=$(/tmp/p196_n16_digits rows.txt "$1" "$2")
 printf '%s\n%s\n' "$a" "$b"
 echo "$a" | grep -q "checksum=$3"
 echo "$b" | grep -q "checksum=$3"
done
echo N16_ALL_REPLAYS_PASS
