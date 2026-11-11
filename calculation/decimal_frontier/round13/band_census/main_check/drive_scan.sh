#!/bin/bash
cd ~/p196_run/mchk13a || exit 1
~/p196_run/venv/bin/python bandscan.py 1000 400 120 6 logs/scan_1000.jsonl > logs/scan_1000.out 2>&1
~/p196_run/venv/bin/python bandscan.py 10 400 120 6 logs/scan_10.jsonl > logs/scan_10.out 2>&1
~/p196_run/venv/bin/python bandscan.py 00001110001 400 120 6 logs/scan_p11.jsonl > logs/scan_p11.out 2>&1
