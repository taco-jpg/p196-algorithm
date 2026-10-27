#!/usr/bin/env python3
"""Complete exact time-first 128-bit B-transfer census: base10, p19, 7 g bits.
Build: c++ -O3 -std=c++17 calculation/agent-8/p19_fixed_g_wide.cpp -o /tmp/a8_p19w
Run: python3 calculation/agent-8/p19_weight7_census.py /tmp/a8_p19w
"""
from collections import Counter
from itertools import combinations
import subprocess
import sys
from time import monotonic

def necklaces(n, weight):
    for positions in combinations(range(n),weight):
        w=''.join('1' if i in positions else '0' for i in range(n))
        if w==min(w[t:]+w[:t] for t in range(n)):
            yield w

def run(exe,g,cap):
    r=subprocess.run([exe,g,str(cap)],capture_output=True,text=True,timeout=30)
    a=r.stdout.strip().split()
    if not a or r.returncode not in (0,3):raise RuntimeError((g,r.stdout,r.stderr,r.returncode))
    kv=dict(x.split('=',1) for x in a[1:] if '=' in x)
    if kv.get('g')!=g:raise RuntimeError('wrong word')
    return a[0],int(kv['states']),int(kv['depth']),r.stdout.strip()

def main():
    exe=sys.argv[1] if len(sys.argv)>1 else '/tmp/a8_p19w'
    start=monotonic();status=Counter();total=0;largest=(0,'');longest=(0,'')
    for g in necklaces(19,7):
        st,states,depth,s=run(exe,g,2_000_000)
        status[st]+=1;total+=states
        largest=max(largest,(states,g));longest=max(longest,(depth,g))
        if st!='EXHAUSTED':print('NONEXHAUSTED',s,flush=True)
    print('P19_WEIGHT7',dict(status),'total_states',total,'max_states',largest,'max_depth',longest,'wall_s',round(monotonic()-start,2))
    if status != Counter({'EXHAUSTED':2652}):sys.exit(1)
    for g in ['11100010000','100010001000']:
        st,states,depth,s=run(exe,g,300000)
        print('POSITIVE',s)
        if st!='ACCEPT':sys.exit(1)
if __name__=='__main__':main()