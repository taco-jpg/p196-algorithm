#!/usr/bin/env python3
"""N28: a four-step non-gauge decimal defect eraser and ordinary-int controls."""
import argparse,json,os,random

def initial(k):
    B=[8]+[16]*79
    h=B+[5,5,2]*k
    return h+[8]+h[::-1]

def positions(m):
    return [80+3*(12+10*j)+1 for j in range(m)]

def implant(p,at):
    q=p[:]
    for s in at:
        assert q[s:s+3]==[5,2,5]
        for j in range(3):
            q[s+j]=7;q[len(q)-1-s-j]=7
    assert q==q[::-1]
    return q

def pair(d):return [d[i]+d[-1-i] for i in range(len(d))]

def initial_digits(p):
    n=len(p);assert n%2 and p[n//2]%2==0
    d=[0]*n
    for i in range(n//2):
        d[i]=p[i]//2;d[n-1-i]=p[i]-d[i]
    d[n//2]=p[n//2]//2
    assert d[-1] and pair(d)==p
    return d

def normalise(p):
    d=[];c=0
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return d

def add_reverse(d):
    out=[];c=0
    for i in range(len(d)):
        z=d[i]+d[-1-i]+c;out.append(z%10);c=z//10
    if c:out.append(c)
    return out

def independent_orbit(p):
    d=initial_digits(p)
    n=int(''.join(map(str,d[::-1])))
    assert list(map(int,str(n)[::-1]))==d and d!=d[::-1]
    trace=[p];gammas=[]
    for t in range(5):
        model=normalise(trace[-1])
        nxt=add_reverse(d)
        assert nxt==model,('independent digit arithmetic',t)
        n+=int(str(n)[::-1])
        assert list(map(int,str(n)[::-1]))==nxt,('independent big integer',t)
        assert nxt!=nxt[::-1],('palindrome',t)
        gammas.append(len(nxt)-len(d))
        d=nxt;trace.append(pair(d))
    assert gammas[:4]==[0,1,0,1],gammas
    return trace,n,gammas

def ca_step(p,g):
    n=len(p);x=[v%9 for v in p];z=[int(v>=10) for v in p]
    q=[x[i]+x[(i-1)%n] if g else
       2*x[i]+z[(i-1)%n]+z[(i+1)%n]-2*z[i] for i in range(n)]
    assert all((1<=v<=8 or 10<=v<=17) for v in q)
    return q

def local_table():
    n=240;s=100
    bg=[5,5,2]*(n//3);q=bg[:]
    assert bg[s:s+3]==[5,2,5]
    q[s:s+3]=[7,7,7]
    expected_q=[[7,7,7],[14,14,14],[6,10,10,6],[13,1,1,13]]
    expected_bg=[[5,2,5],[10,4,10],[2,5,5,2],[4,10,10,4]]
    counts=[3,3,4,4,0];table=[]
    for t in range(5):
        diff=[i for i in range(n) if q[i]!=bg[i]]
        assert len(diff)==counts[t],(t,diff)
        if t<4:
            assert q[s:s+len(expected_q[t])]==expected_q[t]
            assert bg[s:s+len(expected_bg[t])]==expected_bg[t]
        table.append({'t':t,'defect_sites':diff,
                      'base':bg[s:s+4],'particle':q[s:s+4]})
        if t<4:
            bg=ca_step(bg,t%2);q=ca_step(q,t%2)
    assert bg==q
    return table

def verify():
    table=local_table()
    k=80;loc=positions(7);p=initial(k)
    base_trace,base5,base_gamma=independent_orbit(p)
    for bits in range(1<<len(loc)):
        subset=[s for j,s in enumerate(loc) if bits&(1<<j)]
        q=implant(p,subset)
        trace,n5,gs=independent_orbit(q)
        assert gs==base_gamma
        assert trace[4]==base_trace[4],('pairword convergence',bits)
        assert n5==base5,('integer convergence',bits)
    assert [a%9 for a in [5,2,5]]!=[a%9 for a in [7,7,7]]
    wrong=implant(p,[loc[0]])
    for j,v in enumerate((7,7,6)):
        wrong[loc[0]+j]=v
        wrong[len(wrong)-1-loc[0]-j]=v
    assert independent_orbit(wrong)[0][4]!=base_trace[4]
    big=initial(420);bl=positions(40)
    bt,bn,bg=independent_orbit(big)
    rng=random.Random(20261028)
    for _ in range(30):
        q=implant(big,[s for s in bl if rng.randrange(2)])
        qt,qn,qg=independent_orbit(q)
        assert qg==bg and qt[4]==bt[4] and qn==bn
    result={'label':'PAPER PROOF local eraser; COMPUTED arithmetic controls',
      'bulk_period':3,'bulk_temporal_cycle':6,'gamma_first_four':'0101',
      'replacement':{'before':[5,2,5],'after':[7,7,7]},
      'local_trace':table,'pairword_equal_after':4,'integer_equal_after':5,
      'seven_packet_positions':loc,'seed_length':len(p),
      'distinct_variants_checked':128,'additional_40_packet_random_variants':30,
      'negative_control':'[7,7,6] does not heal'}
    print(json.dumps(result,indent=2))
    return p,implant(p,loc)

def write_seed(p,path):
    d=initial_digits(p)
    with open(path,'w') as f:f.write(''.join(map(str,d[::-1]))+'\n')

if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument('--emit-dir',default=None)
    args=a.parse_args()
    p,q=verify()
    if args.emit_dir:
        os.makedirs(args.emit_dir,exist_ok=True)
        write_seed(p,os.path.join(args.emit_dir,'n28_eraser_base.seed'))
        write_seed(q,os.path.join(args.emit_dir,'n28_eraser_seven.seed'))
