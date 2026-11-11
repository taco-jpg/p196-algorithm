#!/bin/bash
# r12b bonus: Theorem U for clocks p11^m, m = 5..8 (L = 55, 66, 77, 88): dumps at K = 300, 301 + wire_unique.py + kstruct.py
cd ~/p196_run/r12b
for L in 55 66 77 88; do
  for K in 300 301; do
    ~/p196_run/r12b/bin/khx3p 10 -g 00001110001 -L $L -batch 4096 -kmax $K -nodecap 100000000 -sec 3000 -dump out/uniq/p11_L${L}_K$K.dump > out/uniq/p11_L${L}_K$K.khx
  done
  echo "== L=$L $(cat out/uniq/p11_L${L}_K300.khx)"
  ~/p196_run/venv/bin/python py/wire_unique.py out/uniq/p11_L${L}_K300.dump out/uniq/p11_L${L}_K301.dump out/uniq/p11_wit.txt | tail -1
  ~/p196_run/venv/bin/python py/kstruct.py --wit out/uniq/p11_wit.txt --L $L out/uniq/p11_L${L}_K300.dump out/uniq/p11_L${L}_K301.dump | grep -E "level 301|ISO"
done
echo P11M_DONE
