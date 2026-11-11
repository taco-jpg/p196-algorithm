#!/bin/bash
# r12b V6: random sample of census words p=41..48 (250 per p): pass-1 khx verdict vs independent kh2 exact (death level must agree).
cd ~/p196_run/r12b
mkdir -p out/v6
for p in 41 42 43 44 45 46 47 48; do
  cat lists/p$p/fc_b10_p${p}_G*.txt | awk -v s=$p 'BEGIN{srand(1000+s)} rand()<0.0002' | head -250 > out/v6/s_p$p.txt
done
cat out/v6/s_p4?.txt > out/v6/sample.txt
~/p196_run/r12b/bin/khx 10 -f out/v6/sample.txt -kmax 400 -nodecap 20000000 -sec 4 > out/v6/khx.out
same=0; diff=0
while read g; do
  p=${#g}
  k1=$(grep -m1 "g=$g " out/v6/khx.out | sed -n 's/.* DIES K=\([0-9]*\).*/\1/p')
  k2=$(nice -n 10 ~/p196_run/r12b/bin/kh2 10 $g $p -exact 400 20000000 | tail -1 | sed -n 's/.* DIES K=\([0-9]*\).*/\1/p')
  if [ -n "$k1" ] && [ "$k1" == "$k2" ]; then same=$((same+1)); else diff=$((diff+1)); echo "DIFF $g khx=$k1 kh2=$k2"; fi
done < out/v6/sample.txt
echo "V6 words=$(wc -l < out/v6/sample.txt) same=$same diff=$diff"
