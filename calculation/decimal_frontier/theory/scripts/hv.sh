#!/bin/bash
# generic: run a script file through heavy and print tail. usage: hv.sh timeout script [args]
t=$1; shift
/home/claude/research/bin/heavy $t "$@"
