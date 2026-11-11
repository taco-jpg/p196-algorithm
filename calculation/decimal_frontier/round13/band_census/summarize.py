#!/usr/bin/env python3
"""Summarize RESULT lines of a log directory (or several) into per-band tables."""
import sys, re, glob, collections
def parse(dirs):
    res=collections.defaultdict(dict)  # key (mode,clock,V,T,epochs,tau) -> rot -> (ans, time, line)
    for d in dirs:
        for f in sorted(glob.glob(d+'/i*.log')):
            for line in open(f):
                if not line.startswith('RESULT'): continue
                m=re.search(r'RESULT (\w\*?) b=(\d+) clock=(\d+) V=([\d,]+) T=(\d+) epochs=(\d+) tau=(\d+) rot=(\d+) word=\[([^\]]*)\] solver=(\w+) trim=(\w+) enc=(\d)(.*): (SAT|UNSAT)',line)
                if not m: print('UNPARSED',line); continue
                mode,b,clk,V,T,ep,tau,rot,word,solver,trim,enc,rest,ans=m.groups()
                tm=re.search(r'total=([\d.]+)s',line); tt=float(tm.group(1)) if tm else -1
                res[(mode,int(b),clk,V,int(T),int(ep),int(tau))][(int(rot),solver,trim=='True',enc,rest.strip())]=(ans,tt,line.strip())
    return res
if __name__=='__main__':
    res=parse(sys.argv[1:])
    for k in sorted(res,key=lambda k:(k[2],len(k[3].split(',')),k[4],k[3])):
        mode,b,clk,V,T,ep,tau=k
        rots=res[k]
        s=len(V.split(','))
        ans_by_rot={}
        for rk,(ans,tt,_) in sorted(rots.items()):
            r=rk[0]
            ans_by_rot.setdefault(r,[]).append(ans)
        allrot=''.join('S' if 'SAT' in ans_by_rot.get(r,[]) else ('U' if ans_by_rot.get(r) else '?') for r in range(s))
        nsat=sum(1 for r in range(s) if 'SAT' in ans_by_rot.get(r,[]))
        print(f'{mode} b={b} clk={clk} s={s} T={T} ep={ep} tau={tau} V={V} rots={allrot} ({nsat}/{s} SAT)')
