#!/usr/bin/env python3
"""Audit of claims made in the r13a report, read-only over logs."""
import re, glob, os, collections
ROOT=os.path.expanduser('~/p196_run/r13a')
print('== 1. cross-census outcomes')
for fn in ['logs/xcensus2.log','logs/xcensus3.log']:
    cur=None; out={}
    for line in open(f'{ROOT}/{fn}'):
        if line.startswith('=='): cur=line.strip(); out[cur]='no CROSS line (alarm/timeout)'
        elif line.startswith('CROSS') and cur: out[cur]=line.strip()
    for k,v in out.items(): print(' ',fn,k,'->',v)
print('== 2. rooted search r=0: TIMEOUT widths')
for i in (0,1):
    f=f'{ROOT}/logs/root2/i0000{i}.log'
    txt=open(f).read()
    print(' ',txt.splitlines()[0][-110:])
    print('   timeouts:',re.findall(r'TIMEOUT tau=\d+ r=(\d+) w=(\d+)',txt))
    print('   summary:',[l for l in txt.splitlines() if l.startswith('ROOTJOB')])
for i in (0,1):
    f=f'{ROOT}/logs/root4/i0000{i}.log'
    if os.path.exists(f):
        txt=open(f).read()
        print('  root4',i,'timeouts:',re.findall(r'TIMEOUT tau=\d+ r=(\d+) w=(\d+)',txt),[l for l in txt.splitlines() if 'ROOT' in l][:3])
print('== 3. contradictions: keys where one method says ALLUNSAT and another finds a SAT rotation')
res=collections.defaultdict(list)
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    for f in glob.glob(d+'/i*.log'):
        for line in open(f):
            if not line.startswith('BANDRESULT'): continue
            m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=(\d+))? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) : rots=(\S+) status=(\w+)',line)
            if m:
                mode,b,clk,V,T,M,TP,tau,R,Rf,solver,enc,rots,st=m.groups()
                res[(mode,clk,V,int(T),int(M),TP,int(tau),int(R))].append((solver,enc,st,rots,os.path.basename(d)))
bad=[];nc=collections.Counter();und=[]
for k,v in res.items():
    if k[0]=='LD': continue
    combos={(s,e) for s,e,st,r,d in v if st=='ALLUNSAT'}
    if not combos: continue
    if any(st=='PASS' for s,e,st,r,d in v): bad.append((k,v))
    nc[len(combos)]+=1
    if len(combos)<3: und.append((k,sorted(combos),[(s,e,st,r) for s,e,st,r,d in v if st!='ALLUNSAT']))
print('  contradictions:',len(bad))
for k,v in bad[:20]: print('   ',k,v)
print('  number of ALLUNSAT keys (non-LD) by number of distinct solver/encoding combos:',dict(nc))
print('  keys with <3 combos (first 25):')
for k,c,o in und[:25]: print('   ',k[0],'clk',k[1],'V',k[2],'T',k[3],'M',k[4],'tau',k[6],c,o)
print('== 4. seam sweep scope')
for tag,jf in [('seam1000a','jobs_seam1000a.txt'),('seam1000b','jobs_seam1000b.txt'),('seam1000c','jobs_seam1000c2.txt')]:
    ts=collections.Counter(re.search(r'--VT (\d+)',l).group(1) for l in open(f'{ROOT}/{jf}') if '--VT' in l)
    print(' ',tag,'jobs by T:',dict(ts))
    lines=[]
    for f in glob.glob(f'{ROOT}/logs/{tag}/i*.log'):
        lines+=[l.strip() for l in open(f) if l.startswith('SEAMBAND') or ': SAT' in l or l.startswith('TIMEOUT')]
    print('   done:',sum('SEAMBAND done' in l for l in lines),'budget:',sum('budget hit' in l for l in lines),'found:',sum('FOUND' in l for l in lines),'sat lines:',sum(': SAT' in l for l in lines),'timeouts:',sum(l.startswith('TIMEOUT') for l in lines))
    for l in lines:
        if 'budget hit' in l: print('    ',l[:100])
print('== 5. proof length in FINAL_head')
s=open(ROOT+'/FINAL_head.md').read()
i=s.index('*Proof (PAPER PROOF).*'); j=s.index('**Theorem GA*',i)
print('  Theorem GA proof: lines',s[i:j].count('\n'),'chars',j-i)
