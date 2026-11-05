#!/bin/bash
cd ~/p196_run/r11c
while kill -0 13984 2>/dev/null || kill -0 13987 2>/dev/null || kill -0 13989 2>/dev/null; do sleep 20; done
exec sat/pool.sh
