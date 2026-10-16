"""All-period pair-language overapproximation of a reverse certificate.

Every directed cycle in the composition graph describes two exact inverse
spatial columns. SCC edges therefore give all predecessor pairs possible
at any temporal period, subject only to the current new-state pair language.
This is an abstraction: if its language grows to include the root, that is
not a root-to-bulk path or a refutation of the exact finite certificate.
"""
from pathlib import Path
from itertools import product
from collections import defaultdict
import json,time

HERE=Path(__file__).resolve().parent
STATES=list(product((0,1),(0,1),(0,1),range(-1,10)))
INDEX={x:i for i,x in enumerate(STATES)}

def inv_options(slot):
    na,nb,nc,nz=slot;out=[]
    for e in (0,1):
        R=nz+10*e
        if not 0<=R<=18 or R<9 and e or R>9 and not e:continue
        for Q,a,b in product(range(19),(0,1),(0,1)):
            if (Q+a)//10!=na:continue
            if (Q+a)%10+(Q+nc)%10!=R:continue
            if (R+b)//10!=nb:continue
            out.append((Q,a,b,(Q+nc)//10,e,R))
    return out

OPTIONS=[inv_options(s)for s in STATES]

def compat(x,y):
    Q,a,b,c,e,R=x
    z=y[0]-(R+b)%10-e
    if z < -1 or z>9 or z==-1 and not e or z==9 and e:return None
    return z

def decode(f,z):
    return tuple(INDEX[tuple((f>>(12*k+j))&1 for k in range(3))+
                       (((z>>(4*j))&15)-1,)]for j in range(12))

def scc(n,edges):
    adj=[[]for _ in range(n)];rev=[[]for _ in range(n)]
    for u,v in edges:adj[u].append(v);rev[v].append(u)
    seen=bytearray(n);order=[]
    for start in range(n):
        if seen[start]:continue
        seen[start]=1;stack=[(start,0)]
        while stack:
            u,k=stack[-1]
            if k==len(adj[u]):order.append(u);stack.pop();continue
            v=adj[u][k];stack[-1]=(u,k+1)
            if not seen[v]:seen[v]=1;stack.append((v,0))
    label=[-1]*n;nc=0
    for start in reversed(order):
        if label[start]>=0:continue
        label[start]=nc;stack=[start]
        while stack:
            u=stack.pop()
            for v in rev[u]:
                if label[v]<0:label[v]=nc;stack.append(v)
        nc+=1
    return label

def closure_pairs(allowed):
    nodes=[];groups=defaultdict(list)
    for new in set(x for p in allowed for x in p):
        for x in OPTIONS[new]:
            for z in range(-1,10):
                old=INDEX[x[1:4]+(z,)]
                for y in OPTIONS[old]:
                    groups[new].append(len(nodes));nodes.append((new,old,x,y))
    edges=[]
    for left,right in allowed:
        for u in groups[left]:
            _,old,x,y=nodes[u];oz=STATES[old][3]
            for v in groups[right]:
                _,old2,x2,y2=nodes[v]
                if compat(x,x2)==oz and compat(y,y2)is not None:edges.append((u,v))
    labels=scc(len(nodes),edges)
    pairs={(nodes[u][1],nodes[v][1])for u,v in edges if labels[u]==labels[v]}
    return pairs,dict(nodes=len(nodes),edges=len(edges),cyclic_edges=sum(labels[u]==labels[v]for u,v in edges))

def main():
    start=time.monotonic()
    lines=(HERE.parent/'reverse/viable_closed_states.txt').read_text().splitlines()[1:]
    words=[decode(*map(int,l.split()))for l in lines]
    allowed={(w[j],w[(j+1)%12])for w in words for j in range(12)}
    root=INDEX[(0,1,1,7)]
    report=[]
    for k in range(20):
        new,stats=closure_pairs(allowed)
        add=new-allowed
        row=dict(iteration=k,allowed_pairs=len(allowed),new_pairs=len(add),
                 root_pair_present=(root,root)in allowed,
                 root_pair_new=(root,root)in add,**stats)
        print(json.dumps(row),flush=True);report.append(row)
        if not add:break
        allowed|=add
    result=dict(iterations=report,closed=not add,
                root_pair_present=(root,root)in allowed,
                seconds=time.monotonic()-start,
                scope='All-period two-letter language overapproximation only; no exterior found')
    (HERE/'pair_language_result.json').write_text(json.dumps(result,indent=2)+'\n')
    (HERE/'pair_language_pairs.json').write_text(json.dumps([[STATES[x],STATES[y]]for x,y in sorted(allowed)])+'\n')
    print(json.dumps({k:v for k,v in result.items()if k!='iterations'}),flush=True)

if __name__=='__main__':main()
