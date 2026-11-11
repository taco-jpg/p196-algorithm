#!/bin/bash
cd ~/p196_run/mchk13a || exit 1
P=~/p196_run/venv/bin/python
{
# clock 1000 exclusions claimed by r13a
$P lcheck.py L 1000 0 --epoch 4 --R 12
$P lcheck.py L 1000 18 --epoch 4 --R 12
$P lcheck.py L 1000 9,18,9,0 --epoch 32 --R 12
$P lcheck.py L 1000 9,18,9,0 --epoch 16 --R 12
$P lcheck.py L 1000 18,9,0 --epoch 40 --R 12
$P lcheck.py L 1000 5,2,1 --tau 16 --epoch 24 --R 12
$P lcheck.py L 1000 11,9,2 --tau 8 --epoch 24 --R 12
$P lcheck.py R 1000 0 --epoch 8 --R 12
$P lcheck.py R 1000 18 --epoch 8 --R 12
$P lcheck.py R 1000 9,18,9,0 --epoch 32 --R 12
# clock 10
$P lcheck.py L 10 0 --epoch 2 --R 12
$P lcheck.py L 10 18 --epoch 2 --R 12
$P lcheck.py L 10 12,9,6 --epoch 6 --R 12
$P lcheck.py L 10 9,12,6 --epoch 6 --R 12
$P lcheck.py L 10 9,18,9,0 --epoch 8 --R 12
$P lcheck.py L 10 12,9,9,6,18,9,0 --epoch 14 --R 12
$P lcheck.py R 10 0 --epoch 4 --R 12
$P lcheck.py R 10 12,9,6 --epoch 12 --R 12
# p11
$P lcheck.py L 00001110001 0 --epoch 11 --R 12
$P lcheck.py L 00001110001 18 --epoch 11 --R 12
# controls that must not be excluded (bands that r13a lists as passing, or the real T12 lattice row)
$P lcheck.py L 1000 5,18,4,8,1,15,4,0,5 --epoch 12 --R 12
$P lcheck.py L 1000 11,8,5 --epoch 24 --R 12
$P lcheck.py L 1000 0 --epoch 4 --R 12 --nofor
} > logs/spot.out 2>&1
echo done >> logs/spot.out
