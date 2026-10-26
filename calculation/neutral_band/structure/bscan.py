import sys, itertools, time
from bauto import run
def necklaces(p):
    seen=set()
    for g in itertools.product('01',repeat=p):
        s=''.join(g)
        rots=[s[i:]+s[:i] for i in range(p)]
        if min(rots)!=s: continue
        yield s
def main():
    b=int(sys.argv[1]); P=int(sys.argv[2])
    for p in range(1,P+1):
        t0=time.time()
        for g in necklaces(p):
            par,acc=run(b,g)
            if acc: print("b",b,"g",g,"ACCEPTED e-streams",sorted(''.join(map(str,e)) for e in acc),"states",len(par),flush=True)
        print("b",b,"p",p,"done",round(time.time()-t0,1),"s",flush=True)
if __name__=="__main__": main()
