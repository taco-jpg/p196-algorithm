"""Exact pair-sum dynamics on a long uniform16 core; diagnostic only."""
import numpy as np, json

def step(q):
    # A q=9 propagates carry; each other coefficient resets it.
    ix=np.where(q!=9,np.arange(len(q)),0)
    np.maximum.accumulate(ix,out=ix)
    out=(q[ix]>=10).astype(np.int8)
    if q[0]==9:
        out[:np.argmax(q!=9)]=0
    c=np.concatenate((np.array([0],dtype=np.int8),out))
    digits=q+c[:-1]-10*c[1:]
    if out[-1]:digits=np.append(digits,np.int8(1))
    return digits+digits[::-1], int(out[-1])

def run(k=20000,steps=10000):
    q=np.full(k+2,16,dtype=np.int8);q[0]=q[-1]=8
    seen={}; repeats=[]; runs=[];flags=[]
    prev=None
    for t in range(steps):
        # A 128-pair window is a diagnostic, never an inductive certificate.
        key=bytes(q[:128]);last=seen.get(key)
        if last is not None:repeats.append((t,last,t-last))
        seen[key]=t
        if t%72==0:
            bg=(16,14,10,2,4,8)[t%6]
            bad=np.flatnonzero(q!=bg)
            mid=len(q)//2
            left=bad[bad<mid]
            width=int(left[-1]+1) if len(left) else 0
            core=max(0,len(q)-2*width)
            runs.append((t,len(q),width,core,list(map(int,q[:12]))))
        q,h=step(q);flags.append(h)
    return {'k':k,'steps':steps,'repeats_128':repeats,'snapshots':runs,'overflow_prefix':''.join(map(str,flags[:500])),'overflow_counts':[sum(flags[i:i+1000]) for i in range(0,steps,1000)]}
if __name__=='__main__':
    out=run();json.dump(out,open('exist_uniform_boundary_results.json','w'),indent=2)
    print(json.dumps({k:v for k,v in out.items() if k!='snapshots'},indent=2))
