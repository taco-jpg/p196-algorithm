#!/usr/bin/env python3
"""Differential test bx vs bauto2 on a random sample of F1-survivor words: cmp_sample.py p nwords seed [cap]"""
import sys,glob,random,subprocess,re,os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p=int(sys.argv[1]); n=int(sys.argv[2]); random.seed(int(sys.argv[3])); cap=sys.argv[4] if len(sys.argv)>4 else '1000000'
ws=[]
for f in glob.glob(f'{ROOT}/lists/fc_b10_p{p}_G*.txt'): ws+=[l.strip() for l in open(f) if l.strip()]
sel=random.sample(ws,n); same=bad=skipped=0; t1=t2=0
import time
for w in sel:
    t=time.time(); r1=subprocess.run([f'{ROOT}/bin/bauto2_w1','10',str(p),str(p),'-g',w,'-cap',cap],capture_output=True,text=True).stdout; t1+=time.time()-t
    t=time.time(); r2=subprocess.run([f'{ROOT}/bin/bx','10','-g',w,'-cap',cap],capture_output=True,text=True).stdout; t2+=time.time()-t
    m=re.search(r'states=(\d+)',r1); st1=int(m[1]) if m and 'STATECAP' not in r1 else None
    m2=re.search(r'(\S+) states=(\d+).* m=(\d+)',r2); status=m2[1]; st2=int(m2[2]); mm=int(m2[3])
    acc1=set(re.findall(r'ACCEPT b=\d+ p=\d+ g=[01]+ e=([01]+)',r1)); acc2=set(re.findall(r' e=([01]+)@',r2))
    if st1 is None or status.startswith('CAPPED'): skipped+=1; continue
    ok=(mm!=1 or st1==st2) and len(acc1)==0==len(acc2) if (acc1 or acc2)==set() else True
    if mm==1 and st1!=st2: bad+=1; print('MISMATCH',w,st1,st2)
    elif bool(acc1)!=bool(acc2): bad+=1; print('ACC MISMATCH',w,acc1,acc2)
    else: same+=1
print(f'p={p}: {n} sampled, {same} identical (states and accept/no-accept), {bad} mismatches, {skipped} skipped (cap); time bauto2 {t1:.1f}s bx {t2:.1f}s')
