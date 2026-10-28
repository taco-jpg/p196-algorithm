#!/bin/bash
cd /home/claude/research/w3_formats/code
python3 kink_sat.py 0 4 8 80 0 2 240 > ../out/ksat_job1.txt 2>&1
python3 kink_sat.py 0 6 8 80 0 1 400 >> ../out/ksat_job1.txt 2>&1
