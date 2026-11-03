#!/bin/bash
cd ~/p196_run/r7
WIN=10 ROT=1 THREADS=6 nice -n 10 ~/p196_run/bands/backdisk 10 24 01 wd_R6U_w10_T24_01 8000000000 0.20 bands allstreams > logs/R6U_w10_T24_01.log 2>&1
