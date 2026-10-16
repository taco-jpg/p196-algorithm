"""Standard-library, independently organized checker of the reverse certificate.

It regenerates inverse local data by exhaustive FORWARD column arithmetic.
Boolean matrix products prove that pruned predecessor prefixes cannot have
a predecessor. This is a finite certificate check, not a bounded search.
"""
from pathlib import Path
from itertools import product, permutations
import json, time, hashlib

HERE = Path(__file__).resolve().parent

def encode_letter(a,b,c,z):
    return (((a*2)+b)*2+c)*11+z+1

def decode_letter(v):
    f,z=divmod(v,11)
    return f//4,(f//2)%2,f%2,z-1

def unpack(f,z):
    return tuple(encode_letter((f>>j)&1,(f>>(12+j))&1,
                              (f>>(24+j))&1,((z>>(4*j))&15)-1)
                 for j in range(12))

def pack(word):
    f=z=0
    for j,v in enumerate(word):
        a,b,c,t=decode_letter(v)
        f|=(a<<j)|(b<<(12+j))|(c<<(24+j))
        z|=(t+1)<<(4*j)
    return f,z

def canonical(word):
    return min(pack(word[j:]+word[:j]) for j in range(12))

def mmul(A,B):
    C=0
    for i,k in product(range(2),repeat=2):
        if any(A&(1<<(2*i+j)) and B&(1<<(2*j+k)) for j in range(2)):
            C|=1<<(2*i+k)
    return C

def build_tables():
    # Derive local inverse fibers by ordinary forward digit normalization.
    fibers=[set() for _ in range(88)]
    for Q,a,b,d,e in product(range(19),range(2),range(2),range(2),range(2)):
        lowcarry,lowdigit=divmod(Q+a,10)
        highcarry,highdigit=divmod(Q+d,10)
        R=lowdigit+highdigit
        if R<9 and e!=0 or R>9 and e!=1:
            continue
        oddcarry,_=divmod(R+b,10)
        zeta=R-10*e
        assert -1<=zeta<=9
        new=encode_letter(lowcarry,oddcarry,d,zeta)
        fibers[new].add((Q,a,b,highcarry,e,R))
    fibers=[tuple(sorted(x))for x in fibers]
    assert sorted(map(len,fibers))==[0]*2+[1]*8+[2]*78
    options=tuple(sorted(set().union(*map(set,fibers))))
    option_id={x:i for i,x in enumerate(options)}
    fibers=[tuple(option_id[x]for x in f)for f in fibers]
    output=[[-1]*len(options)for _ in options]
    for i,x in enumerate(options):
        Q,a,b,c,e,R=x
        for k,y in enumerate(options):
            prior_z=y[0]-((R+b)%10)-e
            # Pending high carry is a decimal digit iff this inequality holds.
            if -1<=prior_z<=9 and 0<=prior_z+e<=9:
                output[i][k]=encode_letter(a,b,c,prior_z)
    matrices=[[0]*88 for _ in range(88)]
    for i,k in product(range(88),repeat=2):
        matrices[i][k]=sum(1<<(2*u+v)
            for u,x in enumerate(fibers[i]) for v,y in enumerate(fibers[k])
            if output[x][y]>=0)
    multiplication=tuple(tuple(mmul(A,B)for B in range(16))for A in range(16))
    return fibers,output,matrices,multiplication

def carries(q,i,direction):
    j=(i+direction)%len(q)
    while q[j]==9:
        j=(j+direction)%len(q)
    return int(q[j]>=10)

def target(B):
    q=B;a=[];b=[];c=[];z=[]
    for t in range(24):
        if t%2:
            b.append(carries(q,0,-1))
            z.append(q[-1]-10*((q[-1]+carries(q,-1,1))//10))
        else:
            a.append(carries(q,0,-1))
            c.append((q[0]+carries(q,0,1))//10)
        h=t%2
        q=tuple((q[i]+carries(q,i,-1))%10+
                (q[(i-h)%3]+carries(q,(i-h)%3,1))%10 for i in range(3))
    assert q==B
    return tuple(encode_letter(*x)for x in zip(a,b,c,z))

def check():
    start=time.monotonic()
    fibers,output,mats,mul=build_tables()
    data=(HERE/'viable_closed_states.txt').read_bytes()
    lines=data.decode().splitlines()
    raw=[tuple(map(int,line.split()))for line in lines[1:]]
    assert len(raw)==int(lines[0]) and len(set(raw))==len(raw)
    C=set(raw)
    words=[unpack(*x)for x in raw]
    assert all(canonical(w)==p for w,p in zip(words,raw))
    def viable(w):
        p=9
        for j in range(12):
            p=mul[p][mats[w[j]][w[(j+1)%12]]]
        return bool(p&9)
    root=(encode_letter(0,1,1,7),)*12
    assert viable(root) and canonical(root) not in C
    targets=[target(B)for B in list(permutations((9,3,6)))+
                                  list(permutations((9,12,15)))]
    assert len(set(targets))==12
    assert len(set(map(canonical,targets)))==2
    assert all(canonical(w)in C for w in targets)
    assert all(viable(w)for w in words)
    live_edges=0;zero_product_prunes=0;nodes=0
    ids={s:i for i,s in enumerate(raw)}
    predecessor_ids=[set()for _ in raw]
    # Check every viable predecessor. The matrix product is carried while
    # assigning old letters so impossible branches are proved dead early.
    for state_index,w in enumerate(words):
        path=[None]*12
        old=[None]*12
        fs=[fibers[x]for x in w]
        def visit(j,boolean_product):
            nonlocal live_edges,zero_product_prunes,nodes
            nodes+=1
            if j==12:
                v=output[path[11]][path[0]]
                if v<0:return
                old[11]=v
                p=mul[boolean_product][mats[old[10]][v]]
                p=mul[p][mats[v][old[0]]]
                if not p&9:return
                live_edges+=1
                key=canonical(tuple(old))
                assert key in C, (state_index,w,old)
                predecessor_ids[state_index].add(ids[key])
                return
            for x in fs[j]:
                path[j]=x
                p=boolean_product
                if j:
                    v=output[path[j-1]][x]
                    if v<0:continue
                    old[j-1]=v
                    if j>=2:
                        p=mul[p][mats[old[j-2]][v]]
                        if p==0:
                            zero_product_prunes+=1
                            continue
                visit(j+1,p)
        visit(0,9)
        if state_index%5000==0:
            print(json.dumps(dict(kind='progress',checked=state_index,
                live_edges=live_edges,seconds=time.monotonic()-start)),flush=True)
    from collections import deque,Counter
    following=[[]for _ in raw]
    for i,ps in enumerate(predecessor_ids):
        for p in ps:following[p].append(i)
    degree=list(map(len,predecessor_ids))
    todo=deque(i for i,d in enumerate(degree)if d==0)
    rank=[0 if d==0 else None for d in degree]
    while todo:
        i=todo.popleft()
        for nxt in following[i]:
            degree[nxt]-=1
            if degree[nxt]==0:
                rank[nxt]=1+max(rank[p]for p in predecessor_ids[nxt])
                todo.append(nxt)
    core=[raw[i]for i,r in enumerate(rank)if r is None]
    core_result=dict(core_orbits=len(core),core_states=core,
                     deletion_rank_histogram=dict(Counter(str(x)for x in rank)),
                     distinct_viable_predecessor_orbit_edges=sum(map(len,predecessor_ids)))
    (HERE/'reverse_core.json').write_text(json.dumps(core_result,indent=2)+'\n')
    result=dict(kind='summary',status='certificate_verified',
        scope='fixed-width alternating 24-phase 8/17 exterior with stated 12 bulk tails',
        certificate_orbits=len(C),targets=len(set(targets)),target_orbits=2,
        viable_predecessor_edges=live_edges,recursion_nodes=nodes,
        zero_product_branch_prunes=zero_product_prunes,
        root_viable=True,root_excluded=True,
        certificate_sha256=hashlib.sha256(data).hexdigest(),
        seconds=time.monotonic()-start,decimal_lychrel_existence_proved=False,
        lean_formalized=False,backward_infinite_core_orbits=len(core),
        deletion_rank_histogram=core_result['deletion_rank_histogram'])
    assert live_edges==40912
    (HERE/'independent_check.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)

if __name__=='__main__':
    check()
