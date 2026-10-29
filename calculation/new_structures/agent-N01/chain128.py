"""N01: exact 128-step decimal two-band finite-horizon identity for every k>=12.
Requires reproduce.py (the separately committed 80-state carry-transducer).
Run: python3 calculation/new_structures/agent-N01/chain128.py
COMPUTED finite-horizon result, NOT a Lychrel certificate.
"""
import reproduce as R

STEPS=128
K=12

def revadd_pair(P):
    d,g=R.normalize(P)
    return tuple(d[i]+d[-1-i] for i in range(len(d))),g,d!=d[::-1]

def evolve(k):
    p=R.source(k);words=[p];overflow=[]
    for _ in range(STEPS):
        p,g,nonpal=revadd_pair(p)
        assert nonpal
        words.append(p);overflow.append(g)
    return words,overflow

def rot(word,offset):
    offset%=len(word)
    return word[offset:]+word[:offset]

def extract(p,k,w,v):
    h=p[:len(p)//2];mid=p[len(p)//2] if len(p)%2 else None
    # The two locked powers remain in fixed, disjoint coordinates.
    first=160;second=20*k-80;third=20*k+536;fourth=68*k-40
    assert len(h)>=fourth and k>=K
    A=rot(w,121);D=rot(v,496)
    assert h[first:second]==A*(k-K)
    assert h[third:fourth]==D*(k-K)
    return (h[:first],A,h[second:third],D,h[fourth:],mid)

def check_edge(left,right,g):
    B,W,J,V,C,centre=left
    b,w,j,v,c,centre1=right
    assert len(B)==len(b)==160 and len(J)==len(j)==616
    M0=R.word(B,b,g);MW=R.word(W,w,g)
    MJ=R.word(J,j,g);MV=R.word(V,v,g)
    if len(C)==len(c):
        MC=R.word(C,c,g);last=centre1
    else:
        assert len(c)==len(C)+1 and centre is not None and centre1 is None
        MC=R.word(C,c[:-1],g);last=c[-1]
    pw=pv=R.ID;seen={};t=0
    while (pw,pv) not in seen:
        assert t<30,'matrix power not proven periodic'
        seen[pw,pv]=t
        M=R.multiply(R.multiply(R.multiply(R.multiply(M0,pw),MJ),pv),MC)
        assert R.accepted(M,g,centre,last,True),('edge mismatch',t)
        pw=R.multiply(pw,MW);pv=R.multiply(pv,MV);t+=1
    return seen[pw,pv],t-seen[pw,pv]

def number_digits(n):
    d=[]
    while n:d.append(n%10);n//=10
    return d

def ordinary_integer_check(states,k=20):
    # Independent BIG INTEGER reverse-and-add. Assert the exact coefficient
    # template and nonpalindromicity at EVERY temporal step, not just endpoints.
    p=R.source(k)
    n=sum(x*10**i for i,x in enumerate(p))
    for t,state in enumerate(states):
        B,W,J,V,C,centre=state
        h=B+W*(k-K)+J+V*(k-K)+C
        template=h+((centre,) if centre is not None else ())+h[::-1]
        assert n==sum(x*10**i for i,x in enumerate(template)),('shape',t)
        d=number_digits(n)
        assert d!=d[::-1],('palindrome',t)
        if t==STEPS:break
        r=sum(d[-1-i]*10**i for i in range(len(d)))
        n+=r
    print('INDEPENDENT BIGINT: k=%d, 129 templates including t=0 and 128 additions, all shapes/no palindromes PASS' % k)

def main():
    samples=[evolve(k) for k in (12,13,14)]
    assert samples[0][1]==samples[1][1]==samples[2][1]
    gamma=samples[0][1]
    assert gamma==[1 if t%2==0 else 0 for t in range(STEPS)]
    w=R.W;v=R.V;states=[]
    for t in range(STEPS+1):
        candidates=[extract(samples[i][0][t],12+i,w,v) for i in range(3)]
        assert candidates[0]==candidates[1]==candidates[2],('factorization',t)
        states.append(candidates[0])
        if t<STEPS:
            w=R.nextbulk(w,gamma[t]);v=R.nextbulk(v,gamma[t])
    periods=[check_edge(states[t],states[t+1],gamma[t]) for t in range(STEPS)]
    assert periods==[(1,1)]*STEPS
    ordinary_integer_check(states,20)
    print('EXACT ALL k>=12: 128 consecutive nonpalindromic reverse-and-add edges, 2 bands of lengths 20 and 48')
    print('ALL 128 joint matrix power pairs: preperiod=1 period=1; centre finite suffix: %d -> %d' % (len(states[0][4]),len(states[-1][4])))
    print('No temporal return or unbounded Lychrel orbit is asserted.')

if __name__=='__main__':main()
