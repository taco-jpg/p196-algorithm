#!/bin/bash
# Build the three binaries (works with g++ or Apple clang++; needs __int128 and C++17).  Run from anywhere.
set -e
cd "$(dirname "$0")/.."
mkdir -p bin out/studio logs lists
CXX=${CXX:-c++}
$CXX -O3 -std=c++17 -DKW=1 -o bin/bx1 src/bx.cpp      # key <= 63 bits (e.g. p=16 G=8 (01)^8, p<=18), 8-byte keys: halves memory
$CXX -O3 -std=c++17 -DKW=2 -o bin/bx  src/bx.cpp      # p<=32 (state key <= 127 bits), 16-byte keys
$CXX -O3 -std=c++17 -DKW=3 -o bin/bx3 src/bx.cpp      # p<=59 (key <= 191 bits), 24-byte keys
$CXX -O3 -std=c++17 -o bin/fc_enum src/fc_enum.cpp    # first-coordinate NFA necklace enumerator
echo built: $(ls bin)
