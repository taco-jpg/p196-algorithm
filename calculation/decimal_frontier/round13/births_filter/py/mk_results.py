#!/usr/bin/env python3
"""mk_results.py: per-word results table for FINAL section 5 (markdown) from the out/ directories. Writes FINAL_results.md."""
import re, glob, os, json
R=os.path.expanduser('~/p196_run/r13c')
F=os.path.join(R,'out')
def collect(tag):
    files=sorted(glob.glob(os.path.join(F,tag,'s*.out')))
    tot=dies=surv=emit=0; shardsdone=0; hist={}; ts=[]; shardsexp=None; maxn=0
    secs=0
    for f in files:
        txt=open(f,errors='ignore').read()
        m=re.search(r'^(KHR|KHR_BULK) .*?shard=(-?\d+)/(\d+).*?(?:emitted=(\d+) )?ran=(\d+) dies=(\d+) surv=(\d+)', txt, flags=re.M)
        if m:
            shardsdone+=1; shardsexp=int(m.group(3)); tot+=int(m.group(5)); dies+=int(m.group(6)); surv+=int(m.group(7))
            if m.group(4): emit+=int(m.group(4))
        for m2 in re.finditer(r'^HIST(.*)$', txt, flags=re.M):
            for kv in m2.group(1).split():
                k,v=kv.split(':'); hist[int(k)]=hist.get(int(k),0)+int(v)
        for m3 in re.finditer(r'^TSURV (.*)$', txt, flags=re.M): ts.append(m3.group(1))
        for m4 in re.finditer(r'maxn=(\d+)', txt): maxn=max(maxn,int(m4.group(1)))
    return dict(nfiles=len(files),done=shardsdone,exp=shardsexp,tot=tot,dies=dies,surv=surv,emit=emit,hist=hist,ts=ts,maxn=maxn)
rows=[('(01)^8','L16',16,8,'22,601 (87)','68,520 / 8,565'),('(01)^12','L24r',24,8,'22,601 (87)','462,450 / ~38,600'),('(01)^16','L32',32,8,'22,601 (87)','3,177,064 / ~198,600'),('(01)^20','L40',40,8,'22,601 (87)','24,071,865 / ~1.2M'),
      ('(0001)^6 = N12^2','N24',24,12,'22,657 (70)','125,090'),('(0001)^9 = N12^3','N36',36,12,'22,657 (70)','1,219,563 / 135,703'),('(0001)^12 = N12^4','N48',48,12,'22,657 (70)','12,489,586 / ~1,040,000'),('(0001)^15 = N12^5','N60',60,12,'22,657 (70)',''),
      ('root 14: (00100101010101)^4','CAP56b',56,14,'337 (15)','826,032'),('root 9: (001010101)^6','CAP54a',54,9,'137 (16)','16,407,243'),('root 11: (00010010111)^5','CAP55a',55,11,'1483 (44)','6,204,780')]
out=[]
out.append('| word | T | d0 | IF(d0) (a0) | births distinct / rotation classes | towers run | die | capped (TSURV) | verdict | max death level | widest level (candidate nodes) |')
out.append('|---|--:|--:|--:|--:|--:|--:|--:|---|--:|--:|')
detail=[]
for name,tag,T,d0,ifc,bc in rows:
    c=collect(tag)
    if c['nfiles']==0: out.append(f'| {name} | {T} | {d0} | {ifc} | {bc} |  |  |  | not run |  |  |'); continue
    complete = (c['exp'] is not None and c['done']>=c['exp'])
    maxk = max(c['hist']) if c['hist'] else 0
    if not complete: verdict = f'PARTIAL (shards {c["done"]}/{c["exp"]})'
    elif c['surv']==0: verdict = 'DIES-primitive'
    else: verdict = f'PARTIAL: {c["surv"]} towers capped'
    out.append(f'| {name} | {T} | {d0} | {ifc} | {bc} | {c["tot"]:,} | {c["dies"]:,} | {c["surv"]} | {verdict} | {maxk} | {c["maxn"]:,} |')
    if c['ts']:
        detail.append(f'**{name}: capped towers (TSURV; UNDECIDED):**')
        for t in c['ts']:
            m=re.match(r'(if=\d+) K=(\d+) kept=(\d+) reason=(\w+) maxn=(\d+) secs=([\d.]+)',t)
            colm=re.search(r'col=([0-9,]+)',t); per=''
            if colm:
                col=[int(x) for x in colm.group(1).split(',') if x!='']; n=len(col); p=next(q for q in range(1,n+1) if n%q==0 and all(col[i]==col[(i+q)%n] for i in range(n)))
                per=f'col_period={p}'
            detail.append(f'  - {m.group(1) if m else t[:30]} K={m.group(2) if m else ""} kept={m.group(3) if m else ""} {m.group(4) if m else ""} {per}')
txt='\n'.join(out)+'\n\n'+'\n'.join(detail)+'\n'

# pass-2 summary
p2=[]
for f in sorted(glob.glob(os.path.join(F,'pass2','*.out'))):
    name=os.path.basename(f)[:-4]; ptxt=open(f,errors='ignore').read()
    ds=re.findall(r'^RDIES idx=\d+ K=(\d+) maxn=(\d+) secs=([\d.]+)',ptxt,flags=re.M); ss=re.findall(r'^RSURV idx=\d+ K=(\d+) kept=(\d+) reason=(\w+)',ptxt,flags=re.M)
    status = 'running' if not re.search(r'^KHR_RUN',ptxt,flags=re.M) else 'finished'
    p2.append(f'- {name}: {status}; dies at K = '+','.join(d[0] for d in ds)+(f' (maxn {ds[0][1]}, {ds[0][2]} s)' if ds else '')+(('; survives/capped: '+'; '.join(f'K={a} kept={b} {c}' for a,b,c in ss)) if ss else ''))
txt=txt+'\n**Pass-2 runs on capped towers (out/pass2/):**\n'+'\n'.join(p2)+'\n'
open(os.path.join(R,'FINAL_results.md'),'w').write(txt)
print(txt[:3000])
