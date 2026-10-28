import sys, subprocess
sys.path.insert(0,'/home/claude/research/w7_kink/code')
from sat_kink import *
def decode(layers, model):
    ms=set(x for x in model if x>0); out=[]
    for lay in layers:
        row=[]
        for sig in lay:
            if sig is None: row.append(None)
            elif isinstance(sig,int): row.append(sig)
            else: row.append([v for v in range(19) if sig[v] in ms][0])
        out.append(row)
    return out
def check(latfn, w, o, mode, N, M=6):
    lat=load_lat(latfn)
    E,layers,K,ns=build(lat,w,o,mode,N,M)
    r,model,dt=solve(E)
    if not r: return 'UNSAT',dt
    dec=decode(layers,model)
    # verify transitions with wtest
    cases=[]
    for t in range(N):
        cases.append(f"{t%lat['p']} {ns[t]} {K} {K} "+' '.join(map(str,dec[t])))
    out=subprocess.run(['./wtest',latfn],input='\n'.join(cases)+'\n',capture_output=True,text=True).stdout.strip().split('\n')
    bad=0
    for t in range(N):
        v=list(map(int,out[t].split()))
        nb=dec[t+1]
        if v[2+2:]!=nb[2:]: bad+=1
    return ('SAT bad=%d'%bad),dt
if __name__=='__main__':
    print(check(sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4],int(sys.argv[5])))
