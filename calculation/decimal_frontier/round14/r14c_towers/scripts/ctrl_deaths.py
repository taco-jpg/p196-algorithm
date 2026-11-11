#!/usr/bin/env python3
# per-tower control: compare ifb death levels with r13c khr death levels on the complete deaths.txt lists
import sys, subprocess
word, g, L, deathsf, outf = sys.argv[1:6]
specs=[]; Ks=[]
for line in open(deathsf):
    parts=line.split()
    if len(parts)<3: continue
    idx, K, spec = parts[0], int(parts[1]), parts[2]
    specs.append(spec); Ks.append(K)
runf=f'ctrl/{word}.runfile'
with open(runf,'w') as f:
    for sp in specs: f.write(f'iface={sp}\n')
res=subprocess.run(['bin/ifb3','10',g,L,'-runfile',runf,'-slots','16777216'],capture_output=True,text=True)
lines=[l for l in res.stdout.splitlines() if l.startswith('TOWER')]
bad=0; n=0; maxk=0; deaths=0; inf=0
for l,K in zip(lines,Ks):
    n+=1
    if ' DIES K=' in l:
        k=int(l.split(' K=')[1].split()[0]); deaths+=1; maxk=max(maxk,k)
        if k!=K: 
            bad+=1
            if bad<5: print('DIFF',l[:120],'r13c K=',K)
    else:
        inf+=1
print(f'{word}: towers compared={n} of {len(Ks)}; ifb deaths={deaths} inf={inf}; maxK={maxk}; mismatches={bad}')
open(outf,'w').write(res.stdout)
