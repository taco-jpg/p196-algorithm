#!/usr/bin/env python3
"""r13a: generate band tables (markdown) from census files and BANDRESULT logs.
usage: mkfinal.py > FINAL_tables.md"""
import sys, re, glob, os
sys.path.insert(0,os.path.expanduser('~/p196_run/r13a'))
import mkjobs as MK
import bandsat as BS
ROOT=os.path.expanduser('~/p196_run/r13a')
CLOCKS=[('1000','clock 1000 (N12 / T12 exterior)'),('10','clock 10 (period-8 lattices)'),('00001110001','clock 00001110001 (p11)')]

def parse_logs():
    res={}
    for d in glob.glob(ROOT+'/logs/*'):
        if not os.path.isdir(d): continue
        for f in glob.glob(d+'/i*.log'):
            for line in open(f):
                if not line.startswith('BANDRESULT'): continue
                m=re.match(r'BANDRESULT (\S+) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+)(?: Tprime=\d+)? tau=(\d+) R=(\d+) Rfree=(\d+) solver=(\w+) enc=(\d) : rots=(\S+) status=(\w+) firstSAT=(\S+) times=\[(.*?)\] total=([\d.]+)s',line)
                if not m: continue
                mode,b,clk,V,T,M,tau,R,Rf,solver,enc,rots,status,first,times,total=m.groups()
                key=(mode,clk,V,int(M),int(tau),int(R))
                res.setdefault(key,[]).append(dict(rots=rots,status=status,solver=solver,enc=enc,total=float(total),file=os.path.basename(d)))
    return res

def bandinfo(clk,V):
    W=[int(x) for x in V.split(',')]
    p=len(clk); cl=[int(c) for c in clk]
    # rows over one F-cycle: compute T from census externally; here just V rows until return
    return W

def rows_cycle(V,clk,b=10):
    p=len(clk); x=list(V); rows=[list(V)]; t=0
    while True:
        y,_,_,_,_=BS.rowstep(rows[-1],int(clk[t%p]),b)
        t+=1
        if y==list(V) and t%p==0:
            break
        rows.append(y)
        if t>200000: break
    return rows,t

def selfmirror(V, clk, T, b=10):
    p=len(clk); x=list(V); n=len(V)
    def palneck(w):
        r=w[::-1]
        return any(all(w[(i+k)%n]==r[i] for i in range(n)) for k in range(n))
    all_ok=True
    for t in range(T):
        if t%p==0 and not palneck(x): all_ok=False
        x,*_=BS.rowstep(x,int(clk[t%p]),b)
    return all_ok

res=parse_logs()
out=[]
counts={}
for clk,title in CLOCKS:
    bands=MK.parse(clk,8)
    out.append(f'\n### 7.{CLOCKS.index((clk,title))+1} {title}: {len(bands)} bands (all spatial periods s <= 8 enumerated; primitive words, up to rotation)\n')
    out.append('| s | V (canonical row, clock phase 0) | T | T_rot/twist | S | #9 | SM | L(M=1) rots | L(1) | L*, Lr, LD, tau-scan (M, status) | R (M) | R* (M) | class | time |')
    out.append('|---|---|---|---|---|---|---|---|---|---|---|---|---|---|')
    nb=0
    for B in sorted(bands,key=lambda B:(B['s'],B['T'],B['V'])):
        V=B['V']; T=B['T']; s=B['s']
        cl=[int(c) for c in clk]
        S=sum(cl[t%len(cl)] for t in range(T))
        nines=sum(1 for v in V.split(',') if v=='9')
        Lres=res.get(('L',clk,V,1,0,12),[])
        L1=next((r for r in Lres),None)
        lrot=L1['rots'] if L1 else '-'
        lstat=L1['status'] if L1 else 'NOTRUN'
        tim=(f"{L1['solver']} {L1['total']:.0f}s" if L1 else '')
        multi=[(k,v) for k,v in res.items() if k[0] in ('L','L*','Lr','Lr*','LD') and k[1]==clk and k[2]==V and (k[3]>1 or k[0] in ('Lr','Lr*','LD') or k[5]!=12 or k[4]!=0)]
        ml=[]; mexcl=False
        for k,v in sorted(multi,key=lambda kv:kv[0][3]):
            st=[x['status'] for x in v]
            status='ALLUNSAT' if 'ALLUNSAT' in st else ('PASS' if 'PASS' in st else 'UNDEC')
            if status=='ALLUNSAT' and k[0]!='LD': mexcl=True
            ml.append(f"{'LD' if k[0]=='LD' else ('Lr' if k[0].startswith('Lr') else 'L')}{'*' if k[0].endswith('*') else ''}M={k[3]}{('R'+str(k[5])) if k[5]!=12 else ''}{('tau'+str(k[4])) if k[4] else ''}:{status}({v[0]['rots']})")
        mstr='; '.join(ml) if ml else '-'
        Rk=[(k,v) for k,v in res.items() if k[0]=='R' and k[1]==clk and k[2]==V]
        Rs=[(k,v) for k,v in res.items() if k[0]=='R*' and k[1]==clk and k[2]==V]
        rstr='-'
        rstat='NOTRUN'
        if Rk:
            k,v=sorted(Rk,key=lambda kv:kv[0][3])[0]
            rstat=v[0]['status']; rstr=f"M={k[3]}:{rstat}({v[0]['rots']})"
        rs='-'
        if Rs:
            k,v=sorted(Rs,key=lambda kv:kv[0][3])[0]
            rs=f"M={k[3]}:{v[0]['status']}({v[0]['rots']})"
        cls='?'
        if lstat=='ALLUNSAT' or mexcl: cls='EXCLUDED(L)'
        elif rstat=='ALLUNSAT': cls='EXCLUDED(R)'
        elif lstat=='PASS' and rstat=='PASS': cls='CAND'
        elif lstat in ('NOTRUN','UNDECIDED') or rstat in ('NOTRUN','UNDECIDED'): cls='UNDEC'
        sm_flag='Y' if selfmirror([int(x) for x in V.split(',')],clk,T) else 'N'
        s_div='d' if S%s==0 else ''
        out.append(f"| {s} | {V} | {T} | {B['Trot']}/{B['twist']} | {S} | {nines} | {sm_flag}{(','+s_div) if s_div else ''} | {lrot} | {lstat} | {mstr} | {rstr} | {rs} | {cls} | {tim} |")
        counts.setdefault(clk,{}).setdefault(cls,0); counts[clk][cls]+=1
# census summary
import collections
print('## 7.0 Census summary (number of bands up to rotation, primitive words)\n')
for clk,title in CLOCKS:
    bands=MK.parse(clk,8)
    bys=collections.Counter(B['s'] for B in bands)
    Ts=collections.Counter(B['T'] for B in bands)
    maxs=max(bys) if bys else 0
    line=' '.join(f"s={k}:{bys[k]}" for k in sorted(bys))
    tline=', '.join(f"{t}x{Ts[t]}" for t in sorted(Ts))
    print(f"- {title}: {sum(bys.values())} bands; {line}")
    print(f"  period T distribution: {tline}")
print()
print('\n'.join(out))
print('\nColumn SM: Y if every phase-0 row of the band is a palindromic necklace (self-mirror; together with s | S the fold closes without a centre, merged-lattice format; the R/R* tests do not apply to such a fold centre), the suffix d marks s divides S (S = overflows per T).\n')
print('\n### Tally (M=1, tau=0, R=12)\n')
for clk,title in CLOCKS:
    print(f'- {title}: {counts.get(clk,{})}')

# ---- machine-generated summary: every ALLUNSAT result (for FINAL.md sec. 6)
print('\n### Explicit list of all bands with an ALLUNSAT result (mode, epochs M, origin tau, R; solver/encoding pairs that report it)\n')
for k in sorted(res.keys(), key=lambda k: (k[1], k[0], len(k[2].split(',')), k[2], k[3], k[4])):
    v = res[k]
    combos = sorted(set(f"{x['solver']}/enc{x['enc']}" for x in v if x['status'] == 'ALLUNSAT'))
    if combos:
        print(f"- {k[0]} clock={k[1]} V={k[2]} M={k[3]} tau={k[4]} R={k[5]}: ALLUNSAT [{', '.join(combos)}]")

# ---- seam and centre sweeps
import re as _re
seam={}; cen={}
for d in glob.glob(ROOT+'/logs/*'):
    if not os.path.isdir(d): continue
    base=os.path.basename(d)
    for f in glob.glob(d+'/i*.log'):
        txt=open(f).read()
        for line in txt.splitlines():
            if line.startswith('SEAMBAND') or line.startswith('RESULT seam') and ': SAT' in line:
                seam.setdefault(f,[]).append(line)
            if line.startswith('CENTREBAND') or line.startswith('CENTRE-SAT'):
                cen.setdefault(f,[]).append(line)
print('\n### Seam sweeps (exterior | J | band; every line = one band sweep; SAT lines are listed verbatim)\n')
if seam:
    print('| job | result |'); print('|---|---|')
    for f in sorted(seam):
        print(f"| {os.path.basename(os.path.dirname(f))}/{os.path.basename(f)} | "+' ; '.join(l[:300] for l in seam[f])+' |')
else:
    print('(none finished yet)')
print('\n### Centre sweeps\n')
if cen:
    print('| job | result |'); print('|---|---|')
    for f in sorted(cen):
        print(f"| {os.path.basename(os.path.dirname(f))}/{os.path.basename(f)} | "+' ; '.join(l[:300] for l in cen[f])+' |')
else:
    print('(none finished yet)')
