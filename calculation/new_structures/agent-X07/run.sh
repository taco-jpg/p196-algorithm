#!/bin/sh
set -eu
cd "$(dirname "$0")"
exe="${TMPDIR:-/tmp}/x07_repdigit_front_$$"
trap 'rm -f "$exe"' EXIT
g++ -O3 -std=c++17 repdigit_front.cpp -lgmpxx -lgmp -o "$exe"
# Independent GMP + schoolbook checks of every exact integer and paired digit.
"$exe" 9 -1 12013 20000
# A finite all-length interval certificate for three distinct perturbations.
"$exe" 9 -1 0 20000
"$exe" 1 3268 0 20000
"$exe" 8 -9999 0 20000
# Independent smaller-length sanity controls.
"$exe" 9 -1 200 40
"$exe" 1 3268 200 40
"$exe" 8 -9999 200 40
