import sys, subprocess, itertools, numpy as np
b=int(sys.argv[1]); TPL='cpp/tpl'
def ev(items, maxs=20000):
    inp='\n'.join(f"{len(B)} {' '.join(map(str,B))} {len(C)} {' '.join(map(str,C))}" for B,C in items)+'\n'
    out=subprocess.run([TPL,'eval',str(b),str(maxs)],input=inp,capture_output=True,text=True).stdout.strip().split('\n')
    return [tuple(map(int,l.split())) for l in out]
nb=b-1; R=range(0,2*b-1)
print('base',b)
# level 1 reference
for m in (4,8,16):
    items=[([B1],[x]+[nb]*m+[x]) for B1 in range(1,2*b-1) for x in R]
    r=ev(items); best=max((o[1],items[i]) for i,o in enumerate(r) if o[0]==0)
    print(' L1 m=%d best %d %s'%(m,best[0],best[1][0]+[0]+best[1][1][:1]))
for a in (4,8,16):
    for m in (4,8,16):
        items=[([B1],[x]+[nb]*a+[y]+[nb]*m+[y]+[nb]*a+[x]) for B1 in range(1,2*b-1) for x in R for y in R]
        r=ev(items); best=max((o[1],items[i]) for i,o in enumerate(r) if o[0]==0)
        nonbreak=sum(1 for o in r if o[0]!=0)
        C=best[1][1]; 
        print(' L2 a=%d m=%d: best lifetime %d  B=%s x=%d y=%d  (size %d) nonbreak %d'%(a,m,best[0],best[1][0],C[0],C[a+1],len(C),nonbreak))
