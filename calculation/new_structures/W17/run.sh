#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -O2 -std=c++17 cell_cone.cpp -o /tmp/w17_cell_cone
/tmp/w17_cell_cone --selftest
/tmp/w17_cell_cone
