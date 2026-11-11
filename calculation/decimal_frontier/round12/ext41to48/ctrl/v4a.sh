#!/bin/bash
# r12b V4a: khx3 -batch 4096 on the V3 sample; its death level must equal the kh2-exact death level recorded in out/v3/part*.cmp
cd ~/p196_run/r12b
cat out/v3/part0*.cmp | grep "::" | awk "{print \$2}" > /tmp/r12b_v4a_in.txt
nice -n 10 bin/khx3 10 -f /tmp/r12b_v4a_in.txt -batch 4096 -kmax 400 -nodecap 3000000 > out/v3/v4a_khx3.out
paste -d" " <(cat out/v3/part0*.cmp | grep "::" | sed "s/.*kh2exact=\[DIES K=\([0-9]*\)\].*/\1/") <(awk "{print \$6}" out/v3/v4a_khx3.out | sed "s/K=//") | awk "{if (\$1==\$2) s++; else {d++; print \"DIFF\", NR, \$0}} END{print \"V4a same\", s, \"diff\", d+0}"
rm -f /tmp/r12b_v4a_in.txt
