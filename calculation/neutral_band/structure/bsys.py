import os
"""Decoupled analysis of the neutral-band dynamics.
B-system: autonomous (the Hyp e1!=e2 forces e2 = 1-e1).
C-system: autonomous on X = digits of C (with carry e1 in, overflow 1-e1 out) -> see csys.py"""
import sys, itertools, collections
sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
import neutral_band_search as N

def norm(b,w,c):
    out=[]
    for v in w:
        out.append((v+c)%b); c=(v+c)//b
    return out,c

def bstep(b,B):
    """one B-step with e2 forced to 1-e1.  returns (B2,u,e1,gam) ; B nonempty, B[0]!=0"""
    DB,e1=norm(b,B,0)
    e2=1-e1
    DR,gam=norm(b,B[::-1],e2)
    if gam==0:
        nb=[x+y for x,y in zip(DB,DR[::-1])]
    else:
        xd=(b-1)*(1-e1)
        nb=[x+y for x,y in zip(DB+[xd],[1]+DR[::-1])]
    u=0
    while nb and nb[-1]==b-1: nb=nb[:-1]; u+=1
    return nb,u,e1,gam

def bgraph(b,nmax):
    """enumerate all B (len<=nmax, B[0]!=0, entries<=2b-2); return dict cycles: canonical cycle -> stream"""
    nxt={}
    for n in range(1,nmax+1):
        for B in itertools.product(range(2*b-1),repeat=n):
            if B[0]==0: continue
            nb,u,e1,gam=bstep(b,list(B))
            nxt[B]=(tuple(nb) if nb and nb[0]!=0 else None,e1,gam,u)
    # find cycles via iterative walk
    state={}  # 0 unvisited,1 in progress,2 done
    cycles={}
    for s in nxt:
        if s in state: continue
        path=[];cur=s
        while True:
            if cur is None or cur not in nxt or cur in state: break
            state[cur]=1; path.append(cur); cur=nxt[cur][0]
        if cur is not None and cur in state and state[cur]==1:
            i=path.index(cur); cyc=path[i:]
            # canonical rotation
            k=min(range(len(cyc)),key=lambda j:cyc[j:]+cyc[:j]); cyc=cyc[k:]+cyc[:k]
            cycles[tuple(cyc)]=tuple((nxt[x][1],nxt[x][2],nxt[x][3]) for x in cyc)
        for x in path: state[x]=2
    return cycles

if __name__=="__main__":
    b=int(sys.argv[1]); nmax=int(sys.argv[2])
    cyc=bgraph(b,nmax)
    print(f"base {b} nmax {nmax}: {len(cyc)} B-cycles")
    streams=collections.Counter()
    for c,s in cyc.items():
        # canonical stream rotation
        k=min(range(len(s)),key=lambda j:s[j:]+s[:j]); s2=s[k:]+s[:k]
        streams[s2]+=1
    for s,cnt in sorted(streams.items(),key=lambda kv:(len(kv[0]),kv[0])):
        print(cnt, ''.join(str(e) for e,g,u in s), ''.join(str(g) for e,g,u in s), "(e1 stream, gam stream)")
    if len(sys.argv)>3:
        for c,s in cyc.items(): print(len(c),c[:3],s)
