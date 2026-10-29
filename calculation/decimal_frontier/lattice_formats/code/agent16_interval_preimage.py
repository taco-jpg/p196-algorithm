#!/usr/bin/env python3
"""Exact integer-interval backward preimage for arbitrary base and fixed cut.
PAPER PROOF method: each transition is affine on three coefficient regimes.
An empty preimage CERTIFIES no full temporal path, hence no outgoing edge.
Nonempty says only that some unclosed temporal path exists, not that x_p=x_0.
"""
import argparse
import json


def union(intervals):
    arr=sorted((a,z) for a,z in intervals if a<=z)
    out=[]
    for a,z in arr:
        if out and a<=out[-1][1]+1:out[-1]=(out[-1][0],max(out[-1][1],z))
        else:out.append((a,z))
    return out


def preimage(b,L,H,g,Y,target):
    """EXACT integer preimage of a union of disjoint integer intervals.
    Each regime/carry piece has y=m*x+k, with m=1 or 2.
    """
    out=[]
    for region,(lo,hi) in enumerate(((0,b-2),(b-1,b-1),(b,2*b-2))):
        for c in (0,1):
            aa=max(lo,H*b-c)
            zz=min(hi,(H+1)*b-1-c)
            if aa>zz:continue
            if g:
                m=1
                k=(L+Y if region==0 else
                   ((b-1+L)%b+Y)-(b-1) if region==1 else
                   L+Y-b)
            else:
                m=2
                k=(L+c if region==0 else
                   ((b-1+L)%b+(b-1+c)%b)-2*(b-1) if region==1 else
                   L+c-2*b)
            for low,high in target:
                a=max(aa,-((k-low)//m))
                z=min(zz,(high-k)//m)
                if a<=z:out.append((a,z))
    return union(out)


def suffix_domains(b,g,L,H,Y):
    """D[t]=all x_t admitting some path to a legal terminal coefficient at p.
    No time closure condition; the absence result is strictly stronger.
    """
    p=len(g)
    assert b>=2 and len(L)==len(H)==p
    y=dict(zip([t for t,bit in enumerate(g) if bit],Y))
    assert len(y)==sum(g)
    sets=[None]*(p+1)
    sets[p]=[(0,2*b-2)]
    for t in range(p-1,-1,-1):
        sets[t]=preimage(b,L[t],H[t],g[t],y.get(t,0),sets[t+1])
    return sets


def diagonal_parent(r,s,j,u,v):
    b=1<<(r+1);p=2*r+4
    L=(1,)*(r+2)+(0,)+(1,)*(j+1)+(0,)*(r-j)
    H=((1,)*(j+1) if s else (0,)+(1,)*j)+(0,)*(r-j)+(u,v)+(1,)*r+(0,)
    Y=(b-2+s,b-(1<<(r-j))-1+u,b-(1<<(r-j))-1+v)
    assert len(L)==len(H)==p
    return L,H,Y


def six_parents(r):
    return ((0,r-2,0,1),(0,r-2,1,1),(0,r-1,1,0),
            (0,r-1,1,1),(1,r-1,0,0),(1,r-1,1,0))


def candidate_starts(b,kind):
    # This is a separately observed candidate list, NOT an all-r proof
    # that other starts have no outgoing temporal path.
    return ((b-16,),(b-14,),(b-6,b-4),(b-5,),(2*b-9,),(2*b-7,))[kind]


def parent_edges(r,source,starts):
    """Exact time-closed paths for specified starts; interval pruning is exact."""
    b=1<<(r+1);p=2*r+4
    L,H,Y=source
    g=[int(i in (0,r+1,r+2)) for i in range(p)]
    y={0:Y[0],r+1:Y[1],r+2:Y[2]}
    result={}
    for x0 in starts:
        domains=[None]*(p+1)
        domains[p]=[(x0,x0)]
        for t in range(p-1,-1,-1):
            domains[t]=preimage(b,L[t],H[t],g[t],y.get(t,0),domains[t+1])
        if not any(a<=x0<=z for a,z in domains[0]):continue
        todo=[(0,x0,(),())]
        while todo:
            t,x,xs,cs=todo.pop()
            if t==p:
                if x==x0:
                    new=(tuple((xs[i]+L[i])//b for i in range(p)),cs,
                         tuple((xs[i]+cs[i])%b for i in (0,r+1,r+2)))
                    result.setdefault(new,[]).append((xs,cs))
                continue
            for c in (0,1):
                if (x+c)//b!=H[t]:continue
                xn=(x+L[t])%b+(y[t] if g[t] else (x+c)%b)
                if any(a<=xn<=z for a,z in domains[t+1]):
                    todo.append((t+1,xn,xs+(x,),cs+(c,)))
    return result


def diagonal_pilot(min_r=4,max_r=1000,check_output=None):
    out=[]
    for r in range(min_r,max_r+1):
        b=1<<(r+1)
        states={};counts=[]
        for k,params in enumerate(six_parents(r)):
            found=parent_edges(r,diagonal_parent(r,*params),candidate_starts(b,k))
            counts.append(len(found));states.update(found)
        assert counts==[4,4,8,8,4,4] and len(states)==32,(r,counts,len(states))
        p=2*r+4;g=[int(i in (0,r+1,r+2)) for i in range(p)]
        maxparts=0;fail_at={}
        for state in states:
            domains=suffix_domains(b,g,*state)
            assert domains[0]==[],('failed empty-domain check',r,state)
            maxparts=max(maxparts,max(map(len,domains)))
            bad=max(i for i,d in enumerate(domains) if not d)
            fail_at[bad]=fail_at.get(bad,0)+1
        row={'r':r,'explicit_successors':32,'empty_fullpath_domains':32,
             'max_disjoint_intervals':maxparts,'first_empty_index_counts':fail_at}
        if check_output:
            with open(check_output,'a') as f:f.write(json.dumps(row)+'\n')
        if r in (4,5,6,7,8,10,20,50,100,200,500,1000) or r==max_r:
            print('PASS terminal-pilot',json.dumps(row,sort_keys=True),flush=True)
        out.append(row)
    return out


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--min-r',type=int,default=4)
    ap.add_argument('--max-r',type=int,default=1000)
    ap.add_argument('--jsonl',default=None)
    args=ap.parse_args()
    diagonal_pilot(args.min_r,args.max_r,args.jsonl)
    print('COMPLETE exact finite controls; all-r reachability remains UNDECIDED')
if __name__=='__main__':main()
