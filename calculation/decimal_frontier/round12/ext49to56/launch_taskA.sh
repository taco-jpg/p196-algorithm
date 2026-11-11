#!/bin/bash
cd ~/p196_run/r12e
( nohup bash run_taskA.sh p34 0001010101001001010101001010100101 "" 15000 > /dev/null 2>&1 < /dev/null & )
( nohup bash run_taskA.sh p47 00010001000110001100010010001010100101000100011 "" 15000 > /dev/null 2>&1 < /dev/null & )
( nohup bash run_taskA.sh p21sq 001001010101001010101 42 15000 > /dev/null 2>&1 < /dev/null & )
