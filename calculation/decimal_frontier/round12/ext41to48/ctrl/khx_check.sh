#!/bin/bash
# r12b: khx -check (every built edge compared with direct trans; every ABSENT wanted edge must have a pruned projection)
# on random samples: 200 words per p=33..40 from the r11 lists (kmax 9) + 200 r11 bx3-capped words that khx kills (kmax 12).
cd ~/p196_run/r12b
for p in 33 34 35 36 37 38 39 40; do
  cut -f2 out/val/r11_p$p.tsv | awk -v s=$p "BEGIN{srand(s)} rand()<0.0005" | head -200 > /tmp/r12b_chk_$p.txt
  echo "p=$p $(nice -n 10 bin/khx 10 -f /tmp/r12b_chk_$p.txt -kmax 9 -nodecap 3000000 -check | grep CHECK | tail -1)"
done
awk "\$3<=12 {print \$2}" out/val/cap_dies.txt | awk "BEGIN{srand(7)} rand()<0.05" | head -200 > /tmp/r12b_chk_cd.txt
echo "capdies $(wc -l < /tmp/r12b_chk_cd.txt) words: $(nice -n 10 bin/khx 10 -f /tmp/r12b_chk_cd.txt -kmax 13 -nodecap 6000000 -check | grep CHECK | tail -1)"
rm -f /tmp/r12b_chk_*.txt
echo CHECK_DONE
