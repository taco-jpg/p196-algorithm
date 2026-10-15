import sys, json, time
from collections import Counter
from complementary_bulk import *


def outer_step(c,B):
    kc=int(c>=10); tc=c-9*kc
    DB,e0=normalize(B,0)
    DRB,gamma=normalize(B[::-1],kc)
    u0=c+e0-10*kc
    Br=add_words(DB+(u0,), (1,)+DRB[::-1] if gamma else DRB[::-1]+(tc,))
    uB=0
    while Br and Br[-1]==2*tc:
        Br=Br[:-1]; uB+=1
    return (2*tc,Br),uB,gamma


def outer_explore():
    starts=[(c, B) for c in PERIODIC_PHASES for B in [()]+[(b,) for b in range(1,19) if b!=c]]
    done={}; cycles=[]; maxlen=0
    for s in starts:
        seen={}; trace=[]
        while s not in seen and s not in done and len(s[1])<=200 and len(trace)<1000:
            seen[s]=len(trace); trace.append(s)
            maxlen=max(maxlen,len(s[1])); s,_,_=outer_step(*s)
        if s in seen:
            cycle=trace[seen[s]:]
            cycles.append(cycle); result=('cycle',len(cycles)-1)
        elif s in done: result=done[s]
        else: result=('cap',s[0],len(s[1]))
        for t in trace: done[t]=result
    print('outer starts',len(starts),'nodes',len(done),'cycles',len(cycles),'maxlen',maxlen)
    print('outer results',Counter(str(done[x]) for x in starts))
    for i,c in enumerate(cycles):
        print('CYCLE',i,'period',len(c),'maxB',max(len(x[1]) for x in c),'gamma',sum(outer_step(*x)[2] for x in c))
        print(c[:20])
    return cycles

if __name__=='__main__': outer_explore()
