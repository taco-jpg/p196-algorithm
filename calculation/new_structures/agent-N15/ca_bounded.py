#!/usr/bin/env python3
"""All-h finite-factor/edge proof for 15 exact decimal dyadic RAA pairword steps.
Only Python standard library.  Standalone, does not import earlier N15 scripts.
"""
from collections import defaultdict

GAMMA=(0,1,1,0,0,0,0,1,0,1,0,1,0,0,1)
STOP=15
R=7
K=77
EDGE=44

def sigma(w):return [z for x in w for z in (x,30-x)]
def w_h(h):
    w=[14]
    for _ in range(h):w=sigma(w)
    return w

def original(h):
    H=[4]+w_h(h)
    return H+H[::-1]

def norm(p):
    d=[];c=0
    for x in p:
        z=x+c;d.append(z%10);c=z//10
    if c:d.append(c)
    return d

def step(p):
    d=norm(p)
    return [d[i]+d[-1-i] for i in range(len(d))],d

def a(x):return int(x>=10)
def H(u,v,w):
    r=2*(u+v-27);s=2*(v+w-27)
    return r+s-9*(a(r)+a(s))

def second_half(h):
    w=w_h(h);m=len(w)+1
    q=[9,9]+[2*(w[i-1]-9) for i in range(2,m)]
    return [10,9,q[2]-10]+[q[i]+q[i-1]-18 for i in range(3,m)]+[2*(q[-1]-9)]

def third(h):
    r=second_half(h)
    g=[1,0,14,5]+[r[i]+r[i-1]-9*(a(r[i])+a(r[i-1])) for i in range(4,len(r))]
    return g+g[::-1]

def factors(length):
    """ALL length-length factors of sigma^R(u v), four u,v options."""
    out=set()
    for u in (14,16):
        for v in (14,16):
            z=[u,v]
            for _ in range(R):z=sigma(z)
            out.update(tuple(z[j:j+length]) for j in range(len(z)-length+1))
    return out

def near(z,index,direction):
    """Carry at cut, scanning back over at most ONE neutral 9."""
    for j in (index,index+direction):
        if j<0 or j>=len(z):raise RuntimeError('boundary entered a bulk window')
        if z[j]!=9:return a(z[j])
    raise RuntimeError('two consecutive neutral 9 coefficients')

def local_update(z,gamma):
    """Exact bulk rule at distance >=3 from BOTH ends when no 99 exists."""
    out=[]
    for i in range(3,len(z)-3):
        lower=near(z,i-1,-1)
        if gamma==0:
            upper=near(z,i+1,1)
            out.append((z[i]+lower)%10+(z[i]+upper)%10)
        else:
            upper=near(z,i,1)
            out.append((z[i]+lower)%10+(z[i-1]+upper)%10)
    return out

def longest9(z):
    run=maxrun=0
    for x in z:
        run=run+1 if x==9 else 0
        maxrun=max(maxrun,run)
    return maxrun

def first_difference(d):
    for i in range(len(d)//2):
        if d[i]!=d[-1-i]:return (i,d[i],d[-1-i])
    return None

def certify_bulk():
    assert K<=1<<R
    fs=factors(K)
    # Finite universal language over blocks sigma^R(u v); any TM factor
    # length <=2^R in a higher iterate lies across <=2 such blocks.
    allowed=defaultdict(set)
    for w in fs:
        z=[H(*w[i:i+3]) for i in range(K-2)]
        for t in range(3,STOP):
            assert longest9(z)<=1,('bulk input carry obstruction',t,w)
            allowed[t].add(z[len(z)//2])
            z=local_update(z,GAMMA[t])
        allowed[STOP].add(z[len(z)//2])
    assert len(fs)==240,len(fs)
    return len(fs),{str(k):sorted(v) for k,v in allowed.items()}

def certify_ends():
    # h=2..9 are all finite exceptional heights; h=10 and 11 represent
    # every later h by the 128-letter prefix and parity suffix rule.
    # Dependency cone after 12 steps is at most 3*12 = 36 columns;
    # source P3 depends on at most 3 initial letters. EDGE+36+3=83<128.
    assert EDGE+3*(STOP-3)+3 < 1<<R
    witnesses={}
    for h in range(2,12):
        p=original(h)
        ww=[]
        for t in range(STOP+1):
            if t==3:assert p==third(h),(h,t,'third formula')
            if 3<=t<STOP:
                assert longest9(p)<=1,(h,t,'end global neutral run')
                assert p[0]!=9,(h,t,'root neutral')
            if t==STOP:break
            p2,d=step(p)
            assert len(p2)-len(p)==GAMMA[t],(h,t,'gamma')
            witness=first_difference(d)
            assert witness is not None,(h,t,'palindrome')
            ww.append(witness)
            if 3<=t<STOP:
                half=len(p)//2
                # This is an INDEPENDENT check of the bounded local formula
                # against whole-pairword normalisation in the actual orbit.
                if half>=7:
                    predicted=local_update(p[:half],GAMMA[t])
                    assert predicted==p2[3:half-3],(h,t,'bulk integer discrepancy')
            p=p2
        witnesses[h]=ww
    # Fixed witness indices t1..15 for all except h=2 at t13.
    assert all(witnesses[h]==witnesses[10] for h in range(3,12))
    assert witnesses[2][12]!=witnesses[10][12]
    # Confirm the end/centre radius windows at every phase agree for a
    # larger higher parity representative; this is an extra numerical guard.
    for h in (12,13):
        ref=10+(h&1)
        p=original(h);q=original(ref)
        for t in range(STOP+1):
            if t>=3:
                wid=min(EDGE,len(q)//2-2)
                assert p[:wid]==q[:wid],(h,t,'lower end')
                assert p[-wid:]==q[-wid:],(h,t,'upper end')
                mp,mq=len(p)//2,len(q)//2
                assert p[mp-wid:mp+wid]==q[mq-wid:mq+wid],(h,t,'centre')
            if t==STOP:break
            p,_=step(p);q,_=step(q)
    return witnesses[10]

def main():
    count,sets=certify_bulk()
    witnesses=certify_ends()
    assert set(sets.keys())=={str(t) for t in range(3,STOP+1)}
    print('TM_BOUNDED_CARRY_ALL_HEIGHTS_PASS', 'all_height_factors',count,
          'sigma_block',1<<R,'original_window',K,
          'edge_dependency_bound',EDGE+3*(STOP-3)+3)
    for t in range(3,STOP+1):print('BULK_T',t,'allowed_center_values',sets[str(t)])
    print('BOUNDARY_PARITY_CLASSES_PASS','h=10,11','finite_exceptions=h2..9',
          'input_max9run<=1 through t14','gamma',''.join(map(str,GAMMA)))
    print('FIRST_UNEQUAL_DECIMAL_DIGITS_t1_to_t15',witnesses)
    print('AGENT_N15_15_STEP_ALL_LEVEL_LOCAL_CERT_PASS')

if __name__=='__main__':main()
