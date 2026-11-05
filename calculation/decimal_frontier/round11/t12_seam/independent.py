#!/usr/bin/env python3
"""Independent full-integer and digit-array checks of the exact central carry cone."""
import random,sys
sys.path.insert(0,__file__.rsplit('/',1)[0])
from cone import B,W,us,outer_clock,centre_step
sys.set_int_max_str_digits(30000)

def pair(ds): return tuple(x+y for x,y in zip(ds,ds[::-1]))
def realize(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i in range(len(p)//2):
        d[i]=max(0,p[i]-9);d[-i-1]=p[i]-d[i]
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1] and all(0<=x<=9 for x in d)
    return d

def step_array(ds):
    out=[];carry=0
    for i in range(len(ds)):
        z=ds[i]+ds[-i-1]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(1)
    return out,carry

def target(U,C,q,k,J):
    h=B+W*q+tuple(J)+tuple(U)*k
    return h+tuple(C)+h[::-1]

def test_one(q,k,U,C,J,check_cones=True):
    p=target(U,C,q,k,J)
    d=realize(p)
    n=int(''.join(map(str,d[::-1])))
    core=list(U)*100+list(C)+list(U[::-1])*100
    central_offset=(len(p)-len(core))//2; actual_off=central_offset
    shift=0;gamma=[]
    clock,_=outer_clock()
    for t in range(120):
        if check_cones:
            pairs=pair(d)
            assert pairs[actual_off:actual_off+len(core)]==tuple(core),(t,'cone mismatch',q,k,U,C,J)
        oldlen=len(d)
        d,carry=step_array(d)
        n+=int(str(n)[::-1])
        assert d==[int(x) for x in str(n)[::-1]],(t,'int versus schoolbook')
        assert len(d)-oldlen==carry==clock[t]
        gamma.append(carry)
        assert d!=d[::-1],(t,'palindrome guard')
        if check_cones:
            core,cut=centre_step(core,carry)
            actual_off+=cut;shift+=cut
    actual=pair(d)
    desired=target(U,C,q,k+5,J)
    assert len(actual)==len(desired) and actual!=desired
    if check_cones:
        assert actual[actual_off:actual_off+len(core)]==tuple(core)
        target_center=tuple(U)*(k+5)+tuple(C)+tuple(U[::-1])*(k+5)
        assert tuple(core)!=target_center[(len(target_center)-len(core))//2:(len(target_center)+len(core))//2]
    return len(p),len(actual),sum(gamma)

def planted_toy():
    # Artificial exact positive target: a real one-step 196 -> 887, not a T* cycle.
    d=[6,9,1]
    nxt,carry=step_array(d)
    assert int(''.join(map(str,d[::-1])))==196
    assert int(''.join(map(str,nxt[::-1])))==887
    exact=pair(nxt)
    assert exact==(15,16,15) and exact!=pair(d)
    return True

def main():
    planted_toy()
    r=random.Random(46)
    sample=[]
    for L in (1,2,3,4,5,6):
        for U in us():
            v=[r.randrange(19) for i in range((L+1)//2)]
            if L%2:v[-1]*=2;v[-1]%=20
            C=tuple(v+(v[::-1] if L%2==0 else v[-2::-1]))
            sample.append((14,100,U,C,tuple(r.randrange(19) for _ in range(r.randrange(9)))))
    for q,k in ((20,120),(40,200),(80,400),(160,800)):
        for L in (1,2,3,4,5,6):
            for U in (us()[0],us()[11],us()[28]):
                v=[r.randrange(19) for i in range((L+1)//2)]
                if L%2:v[-1]=2*r.randrange(10)
                C=tuple(v+(v[::-1] if L%2==0 else v[-2::-1]))
                sample.append((q,k,U,C,tuple(r.randrange(19) for _ in range(r.randrange(35)))))
    for j in (0,1,5,17,50,150,311):
        for L in (1,2,3,4,5,6):
            U=us()[r.randrange(30)]
            C=(4,)*L
            sample.append((14,100,U,C,tuple(r.randrange(19) for _ in range(j))))
    for s in sample:test_one(*s)
    print('PASS','controls=',len(sample),'physical_steps=',len(sample)*120,
          'width_pairs=5','toy_return=1','odd_even_centres=6','J_max=311')

if __name__=='__main__':main()
