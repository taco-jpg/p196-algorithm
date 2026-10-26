import subprocess, re, itertools, sys
from bauto import run
from bscan import necklaces
def canon(g,e):
    p=len(g); best=None
    for r in range(p):
        j=(g[r:]+g[:r], e[r:]+e[:r])
        if best is None or j<best: best=j
    return best
def brute(b,nmax):
    out=subprocess.run(['./bcensus',str(b),str(nmax)],capture_output=True,text=True).stdout
    res=set()
    for m in re.finditer(r"x p(\d+) e=(\d+) g=(\d+) u=(\d+)",out):
        res.add(canon(m[3],m[2]))
    return res
def auto(b,P,nmax):
    res=set()
    for p in range(1,P+1):
        for g in necklaces(p):
            par,acc=run(b,g)
            for e,(s,d) in acc.items():
                if d<=nmax: res.add(canon(g,''.join(map(str,e))))
    return res
for b in range(2,10):
    nmax=5 if b<=8 else 4
    A=auto(b,6,nmax); Bf=brute(b,nmax)
    # brute force only sees primitive cycles up to period with n<=nmax; compare restricted to p<=6
    Bf6={x for x in Bf if len(x[0])<=6}
    print(b,"nmax",nmax,"auto",len(A),"brute",len(Bf6),"equal" if A==Bf6 else ("auto-brute",A-Bf6,"brute-auto",Bf6-A))
