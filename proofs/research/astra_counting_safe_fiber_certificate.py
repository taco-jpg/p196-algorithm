"""Exact certificate for two safe predecessor layers and large G fibers.

The 16-state arithmetic table and suffix closure prove arbitrary length.
Direct integer checks are independent finite controls, not the proof.
"""
from collections import deque
from itertools import product
import json

STATES=tuple(product((0,1),repeat=2))
JOINT=tuple(product(STATES,repeat=2))
ALPHABET=(5,14)
TARGET=((1,1),(1,1))


def local(state,s):
    a,b=state
    ans=[]
    for x in range(19):
        ap,lo=divmod(x+a,10)
        for bp in (0,1):
            bh,hi=divmod(x+bp,10)
            if bh==b and lo+hi==s:
                ans.append(((ap,bp),x))
    return ans


def transition(state,s):
    ans=[]
    for first,x in local(state[0],s):
        for second,y in local(state[1],x):
            ans.append(((first,second),(x,y)))
    assert len(ans)==1,(state,s,ans)
    return ans[0]


def corrections():
    ans={}
    for start in JOINT:
        queue=deque([(start,())]);seen={start}
        while queue:
            st,path=queue.popleft()
            if st==TARGET:
                break
            for symbol in ALPHABET:
                nxt,_=transition(st,symbol)
                if nxt not in seen:
                    seen.add(nxt);queue.append((nxt,path+(symbol,)))
        assert st==TARGET and len(path)<=6
        ans[start]=path+(14,)*(6-len(path))
        st=start
        for symbol in ans[start]:st,_=transition(st,symbol)
        assert st==TARGET
    return ans


def step(q):
    digits=[];carry=0
    for x in q:
        carry,z=divmod(x+carry,10);digits.append(z)
    if carry:digits.append(carry)
    return tuple(x+y for x,y in zip(digits,reversed(digits))),carry


def palindrome_producing(q):
    return all(x<=9 for x in q) or (q[0]==11 and all(x in (0,11) for x in q))


def realize(q):
    d=[0]*len(q)
    for i in range(len(q)//2):
        d[i]=max(0,q[i]-9);d[-i-1]=min(9,q[i])
    return sum(digit*10**i for i,digit in enumerate(d))


def make(w,k,fix):
    state,labels=transition(((0,0),(0,0)),14)
    assert labels==(7,3)
    for symbol in w:state,_=transition(state,symbol)
    half=(14,)+w+fix[state]+(18,)*k
    state=((0,0),(0,0));h1=[];h0=[]
    for symbol in half:
        state,(x,y)=transition(state,symbol)
        h1.append(x);h0.append(y)
    assert state==TARGET
    q2=half+half[::-1]
    q1=tuple(h1+h1[::-1]);q0=tuple(h0+h0[::-1])
    r=(5,)+(10,)*(len(w)+6)+(14,)+(18,)*(2*k-1)+(14,)+(10,)*(len(w)+6)+(5,)
    assert step(q0)==(q1,0)
    assert step(q1)==(q2,0)
    assert step(q2)==(r,1)
    assert all(not palindrome_producing(q) for q in (q0,q1,q2))
    z=r
    for _ in range(k):
        assert not palindrome_producing(z)
        z,_=step(z)
    n=realize(q0)
    orbit=[n]
    for _ in range(k+3):orbit.append(orbit[-1]+int(str(orbit[-1])[::-1]))
    assert all(str(v)!=str(v)[::-1] for v in orbit)
    assert tuple(int(a)+int(b) for a,b in zip(str(orbit[3]),reversed(str(orbit[3]))))==r
    return dict(word=list(w),correction=list(fix[transition_after_word(w)]),q0=list(q0),q1=list(q1),q2=list(q2),r=list(r),seed=str(n),orbit=[str(x) for x in orbit])


def transition_after_word(w):
    state,_=transition(((0,0),(0,0)),14)
    for symbol in w:state,_=transition(state,symbol)
    return state


def main():
    fix=corrections()
    assert all(len({transition(st,s)[0] for st in JOINT})==16 for s in ALPHABET)
    assert transition(TARGET,14)[0]==TARGET
    assert transition(TARGET,18)==(TARGET,(18,18))
    cert=[]
    for st in JOINT:
        cert.append(dict(state=st,edges=[dict(symbol=s,next=transition(st,s)[0],ancestor_symbols=transition(st,s)[1]) for s in ALPHABET],correction=fix[st]))
    checked=0;samples=[]
    for m in range(9):
        for k in range(1,6):
            common=None
            seeds=set()
            for w in product(ALPHABET,repeat=m):
                row=make(w,k,fix)
                merged=row['orbit'][4]
                if common is None:common=merged
                assert merged==common
                assert row['seed'] not in seeds
                seeds.add(row['seed']);checked+=1
                if m==2 and k==2:samples.append(row)
            assert len(seeds)==2**m
    result=dict(status='exact 16-state finite certificate; arbitrary word length theorem',free_symbols=ALPHABET,correction_length=6,target_state=TARGET,certificate=cert,integer_controls=dict(max_free_length=8,future_horizons=[1,2,3,4,5],checked=checked),samples=samples)
    with open('astra_counting_safe_fiber_certificate.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps({k:v for k,v in result.items() if k not in ('certificate','samples')},indent=2))
    print('Sample seeds:',[x['seed'] for x in samples])


if __name__=='__main__':main()
