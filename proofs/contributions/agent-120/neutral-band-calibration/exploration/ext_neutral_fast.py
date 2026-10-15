import sys, itertools, time
from ext_neutral import make
b=int(sys.argv[1]); maxlen=int(sys.argv[2]); cap=int(sys.argv[3])
E=make(b); n=b-1
outcome={}   # state -> 'G' (grows past cap) or cycle id
cycles=[]
t0=time.time(); count=0
for m in range(0,maxlen+1):
    for B in itertools.product(range(2*b-1),repeat=m):
        if m and (B[0]==0 or B[-1]==n): continue
        count+=1
        path=[]; idx={}; cur=tuple(B)
        while True:
            if cur in outcome: res=outcome[cur]; break
            if cur in idx:
                cyc=path[idx[cur]:]; cid=len(cycles); cycles.append(cyc); res=('C',cid)
                for s in cyc: outcome[s]=res
                break
            if len(cur)>cap: res='G'; break
            idx[cur]=len(path); path.append(cur)
            cur=E(cur)[0]
        for s in path:
            if s not in outcome: outcome[s]=res
print('base',b,'maxlen',maxlen,'cap',cap,'starts',count,'cycles',len(cycles),'states',len(outcome),round(time.time()-t0,1),'s')
for c in cycles[:20]:
    print(len(c), c[:4])
