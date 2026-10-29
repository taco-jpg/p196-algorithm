#!/bin/sh
set -eu
cd "$(dirname "$0")"
g++ -std=c++17 -O3 -Wall -Wextra -Wno-unused-function -Wno-unused-variable -Wno-return-type front_check.cpp -o /tmp/n27_front_check
/tmp/n27_front_check 40 10000 1000
/tmp/n27_front_check 80 10000 1000
/tmp/n27_front_check 200 10000 1800
/tmp/n27_front_check 500 10000 4000
/tmp/n27_front_check 3000 12000 21000
python3 independent_front.py 80 1000 500
python3 independent_front.py 200 1000 600
