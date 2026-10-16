"""Small exact algebraic and forbidden-factor checks for boundary research.

The all-width/all-period conclusion additionally needs the independent
sofic preimage and G8=G5 certificate checked in the reverse/ subdirectory.
This file independently verifies local inverse formulas, a compatible
modulo-nine charge, and short root-label ranking certificates for G0..G7.
"""
from pathlib import Path
from itertools import product, permutations
from collections import Counter, deque
import hashlib,json

HERE=Path(__file__).resolve().parent
REVERSE=HERE.parent/'reverse'
LETTERS=list(product((0,1),(0,1),(0,1),range(-1,10)))
ROOT=(0,1,1,7)

def encode(x):
    a,b,c,z=x
    return ((a*2+b)*2+c)*11+z+1

def inverse_direct(new):
    alpha,beta,delta,zeta=new
    result=set()
    for Q,a,b,e in product(range(19),(0,1),(0,1),(0,1)):
        alpha2,low=divmod(Q+a,10)
        c,high=divmod(Q+delta,10)
        R=low+high
        if R<9 and e or R>9 and not e:continue
        beta2=(R+b)//10
        if (alpha2,beta2,delta,R-10*e)==new:
            result.add((Q,a,b,c,e,R))
    return result

def inverse_formula(new):
    alpha,beta,delta,zeta=new
    if 0<=zeta<=8:
        R=zeta+10*beta;e=beta;bs=(0,1)
    else:
        assert zeta in (-1,9)
        R=9;e=(9-zeta)//10;bs=(beta,)
    result=set()
    a=(R-delta)%2
    Q=10*alpha+(R-delta-a)//2
    if 0<=Q<=18:
        for b in bs:result.add((Q,a,b,alpha,e,R))
    if R==9 and alpha!=delta:
        for b in bs:result.add((9,alpha,b,delta,e,R))
    return result

def F(x):
    a,b,c,z=x
    return 11*a+10*b-110*c+10*z

def charge(state):
    return sum(pow(7,j,9)*(2*a+b-2*c+z)
               for j,(a,b,c,z)in enumerate(zip(*state)))%9

def target(B):
    q=tuple(B);a=[];b=[];c=[];z=[]
    def incoming(q,i,d):
        k=(i+d)%3
        while q[k]==9:k=(k+d)%3
        return int(q[k]>9)
    for t in range(24):
        if t%2:
            b.append(incoming(q,0,-1))
            z.append(q[-1]-10*((q[-1]+incoming(q,-1,1))//10))
        else:
            a.append(incoming(q,0,-1))
            c.append((q[0]+incoming(q,0,1))//10)
        h=t%2
        q=tuple((q[i]+incoming(q,i,-1))%10+
                (q[(i-h)%3]+incoming(q,(i-h)%3,1))%10
                for i in range(3))
    assert q==B
    return a,b,c,z

def ranks(graph):
    n=graph['vertices'];edges=graph['edges'];root=encode(ROOT)
    selected=[(u,v)for u,v,label in edges if label==root]
    adj=[[]for _ in range(n)];ind=[0]*n
    for u,v in selected:adj[u].append(v);ind[v]+=1
    queue=deque(u for u in range(n)if not ind[u]);rank=[0]*n;seen=0
    while queue:
        u=queue.popleft();seen+=1
        for v in adj[u]:
            rank[v]=max(rank[v],rank[u]+1);ind[v]-=1
            if not ind[v]:queue.append(v)
    assert seen==n
    assert all(0<=x<=2 for x in rank)
    assert all(rank[u]<rank[v] for u,v in selected)
    # The checker may consume this sparse list with implicit zero elsewhere.
    sparse=[[i,r]for i,r in enumerate(rank)if r]
    replay=[0]*n
    for i,r in sparse:replay[i]=r
    assert all(replay[u]<replay[v]for u,v in selected)
    return dict(root_edges=len(selected),maximum_root_path=max(rank,default=0),
                sparse_rank=sparse)

def main():
    counts=Counter();empty=[]
    for new in LETTERS:
        direct=inverse_direct(new);formula=inverse_formula(new)
        assert direct==formula
        counts[len(direct)]+=1
        if not direct:empty.append(new)
    assert counts=={0:2,1:8,2:78}
    identities=0
    for old in LETTERS:
        a,b,c,z=old
        for Q,d,e in product(range(19),(0,1),(0,1)):
            if (Q+d)//10!=c:continue
            ap,lo=divmod(Q+a,10)
            R=lo+Q+d-10*c
            if not 0<=R<=18:continue
            if R<9 and e or R>9 and not e:continue
            if not 0<=z+e<=9:continue
            bp,olow=divmod(R+b,10)
            Qnext=olow+z+e
            if not 0<=Qnext<=18:continue
            new=(ap,bp,d,R-10*e)
            assert 10*Qnext-22*Q==F(old)-10*F(new)+99*(new[3]-11*d)
            identities+=1
    root_state=tuple(tuple(x for _ in range(12))for x in ROOT)
    assert charge(root_state)==0
    Bs=sorted(set(permutations((9,3,6)))|set(permutations((9,12,15))))
    charges=[dict(bulk=B,charge=charge(target(B)))for B in Bs]
    assert all(row['charge']==0 for row in charges)
    graph_ranks=[]
    for k in range(8):
        p=REVERSE/f'sofic_depth_{k}.json';data=p.read_bytes();g=json.loads(data)
        row=dict(depth=k,vertices=g['vertices'],edges=len(g['edges']),
                 graph_sha256=hashlib.sha256(data).hexdigest(),**ranks(g))
        graph_ranks.append(row)
    fixed_graph_equality=json.loads((REVERSE/'sofic_depth_8.json').read_text())==json.loads((REVERSE/'sofic_depth_5.json').read_text())
    assert fixed_graph_equality
    certificate=dict(root_letter=ROOT,root_code=encode(ROOT),rank_bound=2,
                     forbidden_temporal_factor=[ROOT]*3,graphs=graph_ranks)
    (HERE/'root_factor_rank_certificate.json').write_text(json.dumps(certificate,indent=2)+'\n')
    report=dict(inverse_fibers_checked=88,inverse_fiber_sizes=dict(counts),
                empty_fibers=empty,local_integer_identities_checked=identities,
                root_mod9_charge=0,target_mod9_charges=charges,
                root_rank_checks=[{k:v for k,v in row.items()if k not in ('sparse_rank','graph_sha256')}for row in graph_ranks],
                graph8_equals_graph5=fixed_graph_equality,
                scope='Local algebra and forbidden root factor certified; exact sofic preimages checked separately in reverse/',
                finite_exterior_constructed=False,decimal_lychrel_existence_proved=False)
    (HERE/'structural_checks_result.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
