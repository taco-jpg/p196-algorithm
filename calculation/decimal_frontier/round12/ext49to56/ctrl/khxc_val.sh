#!/bin/bash
# r12e: validate khxc (streaming/summary census driver) against khx (r12b build) on a sample of p41 words
# (every 10th F1 necklace of length 41) + the 66 r12b census pass-1 survivors (p41..48).
cd ~/p196_run/r12e/scratch/t
A="-kmax 400 -nodecap 20000000 -sec 4"
awk 'NR%10==1' all41.txt > s41.txt
cat ~/p196_run/r12b/out/census/surv_p4*.txt | awk '{for(i=1;i<=NF;i++) if($i ~ /^g=/) print substr($i,3)}' > surv.txt
cat s41.txt surv.txt > val_in.txt
wc -l s41.txt surv.txt val_in.txt
nice -n 10 ../../bin/khx 10 -f val_in.txt $A > o_khx.txt &
nice -n 10 ../../bin/khxc 10 -f val_in.txt $A > o_khxc.txt &
nice -n 10 ../../bin/khxc 10 -f val_in.txt $A -summary -krep 40 -samp 1000 > o_sum.txt &
wait
awk '{print $4, $5, ($5=="DIES") ? $6 : ""}' o_khx.txt > a1
awk '{print $4, $5, ($5=="DIES") ? $6 : ""}' o_khxc.txt > a2
cmp a1 a2 && echo VERDICTS_SAME
tail -1 o_sum.txt
echo "sampled lines: $(grep -c samp o_sum.txt)  survivors khx: $(grep -c SURVIVES o_khx.txt)  summary non-samp lines: $(grep -vc samp o_sum.txt)"
echo -n "khx hist: "; awk '$5=="DIES"{split($6,a,"="); h[a[2]+0]++} END{for(k in h) printf "%s:%d\n", k, h[k]}' o_khx.txt | sort -n | tr '\n' ','; echo
