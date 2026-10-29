#!/bin/sh
set -eu
p=calculation/new_structures/agent-W19
bin=$(mktemp -d)
trap 'rm -rf "$bin"' EXIT
g++ -O3 -std=c++17 -Wall -Wextra -Werror "$p/universal_guard.cpp" -o "$bin/guard"
"$bin/guard"
python3 "$p/universal_guard_int.py"
printf '%s\n' 'W19_UNIVERSAL_GUARD_ALL_PASS'
