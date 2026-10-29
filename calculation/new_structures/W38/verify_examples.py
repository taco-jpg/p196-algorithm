#!/usr/bin/env python3
"""Independent bigint/digit-array controls and R30 symbolic checks for W38."""
from pathlib import Path
import re
import sys
sys.set_int_max_str_digits(0)
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'calculation'/'new_structures'/'R30'))
from parametric import load_lattice, replay_symbolic, tpl, step

LATTICE=ROOT/'calculation'/'decimal_frontier'/'lattice_kinks'/'data'/'lat_p12m9.txt'
B,W,_=load_lattice(LATTICE)
CPP=(Path(__file__).with_name('screen.cpp')).read_text()
def cpp_word(name):
    m=re.search(r'static const V '+name+r'=\{([^}]*)\};',CPP)
    assert m,('missing C++ word',name)
    return [int(x.strip()) for x in m.group(1).split(',')]
assert cpp_word('B')==B and cpp_word('W')==W and cpp_word('U')==[9,16,2] and cpp_word('C')==[0,16,0]
U=[9,16,2]
JS=([3,0,0],[0,0,3],[0,0,0,3])
WIDTHS=(20,40,80,160)
J_RAW=19**3+19**4
C_RAW=10*sum(19**r for r in range(1,7))
C_GATED=sum(19**r for r in range(1,7))
assert (J_RAW,C_RAW,C_GATED,J_RAW*C_RAW,C_GATED*(626+11844)) == (137180,496595400,49659540,68122956972000,619254463800)
print('SEARCH_SPACE_PASS raw_pairs=68122956972000 gated_pairs=619254463800 J_words=12470')

def template_pair(J,C,q,k):
    h=B+W*q+list(J)+U*k
    return h+list(C)+h[::-1]

def realize_digits(p):
    assert p==p[::-1]
    d=[0]*len(p)
    for i,x in enumerate(p[:len(p)//2]):
        hi=min(9,x);d[i]=x-hi;d[-1-i]=hi
    if len(p)%2:
        assert p[len(p)//2]%2==0
        d[len(p)//2]=p[len(p)//2]//2
    assert d[-1]>0
    return d

def vector_step(d):
    out=[];carry=0;n=len(d)
    for i in range(n):
        z=d[i]+d[n-1-i]+carry
        out.append(z%10);carry=z//10
    if carry:out.append(carry)
    return out

def vector_run(J,C,q,k):
    d=realize_digits(template_pair(J,C,q,k));gam=[]
    for _ in range(120):
        nd=vector_step(d);gam.append(len(nd)-len(d));d=nd
    got=[d[i]+d[-1-i] for i in range(len(d))]
    h=B+W*q+list(J)+U*(k+5);target=h+list(C)+h[::-1]
    fm=next((i for i,(x,y) in enumerate(zip(got,target)) if x!=y),None)
    if fm is None and len(got)!=len(target):fm=min(len(got),len(target))
    cut=len(B)+9*q
    return ''.join(map(str,gam)),fm,got==target,got[:cut]==target[:cut],len(d)

def bigint_run(J,C,q,k):
    d=realize_digits(template_pair(J,C,q,k));n=int(''.join(map(str,d[::-1])));gam=[]
    for _ in range(120):
        s=str(n);n2=n+int(s[::-1]);gam.append(len(str(n2))-len(s));n=n2
    s=str(n);got=[int(s[-1-i])+int(s[i]) for i in range(len(s))]
    h=B+W*q+list(J)+U*(k+5);target=h+list(C)+h[::-1]
    fm=next((i for i,(x,y) in enumerate(zip(got,target)) if x!=y),None)
    if fm is None and len(got)!=len(target):fm=min(len(got),len(target))
    cut=len(B)+9*q
    return ''.join(map(str,gam)),fm,got==target,got[:cut]==target[:cut],len(s)

def bulk_signature(J,C):
    # The q/k-powered run words at every exact R30 symbolic phase; every block must reset carry.
    cur=tpl(B,W,list(J),U,list(C));sig=[];q_occ=k_occ=0
    for t in range(121):
        qw=tuple(sorted((r.word,r.n.q) for r in cur if r.n.q))
        kw=tuple(sorted((r.word,r.n.k) for r in cur if r.n.k))
        assert all(any(x!=9 for x in w) for w,_ in qw),('all-9 W run',t,qw)
        assert all(any(x!=9 for x in w) for w,_ in kw),('all-9 U run',t,kw)
        q_occ+=len(qw);k_occ+=len(kw);sig.append((qw,kw))
        if t<120:cur,_=step(cur,512,512)
    assert q_occ==242 and k_occ==242,(q_occ,k_occ)
    return tuple(sig)

cases=0
for L in (3,5,7,9,11,13):
    r=(L-1)//2;mid=16 if r%2 else 6
    C=[0]*r+[mid]+[0]*r
    assert C==C[::-1] and C[r]%2==0
    for J in JS:
        aJ=sum((1 if i%2==0 else -1)*x for i,x in enumerate(J))
        assert aJ%11==(3 if len(J)==3 else 8)
        for q in WIDTHS:
            a=vector_run(J,C,q,q);b=bigint_run(J,C,q,q)
            assert a==b,(J,C,q,a,b)
            assert a[0]=='1000'*30 and a[1] is not None and not a[2] and not a[3]
            assert -25<=a[1]-(len(B)+9*q)<=-15,(J,C,q,a)
            cases+=1
print(f'BIGINT_VS_DIGIT_ARRAY_PASS cases={cases} (3 J representatives x 6 odd-centre lengths x 4 widths x 120 edges)')

sigs=[]
for J in ([3,0,0],[0,0,3],[0,0,0,3]):
    out=replay_symbolic(B,W,list(J),U,[0,16,0],512,512,120)
    assert not out['return'] and out['clock_exact'] and out['odd_witnesses_complete'],(J,out)
    assert out['first_mismatch'] in ('9q+0k+11','9q+0k+12'),(J,out)
    print('R30_SYMBOLIC_PASS',J,'first_mismatch='+out['first_mismatch'],'observed=',out['observed'],'expected=',out['expected'])
    for L in (3,5,7,9,11,13):
        r=(L-1)//2;mid=16 if r%2 else 6;C=[0]*r+[mid]+[0]*r
        sigs.append(bulk_signature(J,C))
        if J==[3,0,0]:
            outc=replay_symbolic(B,W,list(J),U,C,512,512,120)
            assert not outc['return'] and outc['first_mismatch']=='9q+0k+11' and outc['clock_exact'] and outc['odd_witnesses_complete'],(J,C,outc)
assert all(sig==sigs[0] for sig in sigs), 'bulk phase words unexpectedly depend on J or centre length'
print('R30_BULK_RESET_PASS traces=18 states_per_trace=121 W_run_occurrences=242 U_run_occurrences=242 all9_runs=0')
print('R30_ALL_CENTRE_LENGTHS_PASS representative_J=[3,0,0] lengths=3,5,7,9,11,13 first_mismatch=9q+11')
print('W38_INDEPENDENT_CONTROLS_PASS')
