import itertools, subprocess, sys, time, re
from ctest import brute
from cauto2 import lengths
def sweep(b, Ps, m0max, tl, extra=()):
    t0=time.time(); ncase=0; nfeas=0; bad=0
    for P in Ps:
        for g in itertools.product((0,1),repeat=P):
            G=sum(g)
            if G==0 or G%2: continue
            for e in itertools.product((0,1),repeat=P):
                if time.time()-t0>tl: return ncase,nfeas,bad,'timeout'
                es=''.join(map(str,e)); gs=''.join(map(str,g))
                out=subprocess.run(['./cauto',str(b),es,gs,'1',str(m0max),'-vall'],capture_output=True,text=True).stdout
                got={(m.group(1),int(m.group(2))) for m in re.finditer(r"FEASIBLE .* v=(\d+) m0=(\d+)",out)}
                exp=set()
                for pos in itertools.combinations(range(P),G//2):
                    v=[1 if t in pos else 0 for t in range(P)]
                    for m0 in range(1,m0max+1):
                        if lengths(list(g),v,m0) is None: continue
                        ncase+=1
                        if brute(b,list(e),list(g),m0,v)>0: exp.add((''.join(map(str,v)),m0))
                nfeas+=len(exp)
                if got!=exp: bad+=1; print("MISMATCH",b,es,gs,"cpp-only",got-exp,"brute-only",exp-got)
    return ncase,nfeas,bad,'done'
b=int(sys.argv[1]); Ps=[int(x) for x in sys.argv[2].split(',')]
print(b,Ps,sweep(b,Ps,int(sys.argv[3]),float(sys.argv[4])))
