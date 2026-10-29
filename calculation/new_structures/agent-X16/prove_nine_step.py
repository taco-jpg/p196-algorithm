#!/usr/bin/env python3
"""Exact finite checker for all-width nine-step Thue-Morse port reset.
No infinite decimal Lychrel or Lean claim.
Run: python3 calculation/new_structures/agent-X16/prove_nine_step.py
"""
import json
SIG={"0":"01","1":"10"}
EXC={"001101","101100"}

def sub(w):
    return "".join(SIG[z] for z in w)

def factors(L):
    s="0"
    while True:
        if len(s)>=L:
            W={s[i:i+L] for i in range(len(s)-L+1)}
            # Explicit closure under every length-L window in sigma(w).
            if all(sub(w)[i:i+L] in W for w in W for i in range(L+1)):
                return W,len(s)
        s=sub(s)

def norm(p,c):
    out=[]
    for x in p:
        s=x+c;out.append(s%10);c=s//10
    return out

def prefix_step(p,g,hi_in):
    lo=norm(p,0);hi=norm(p[::-1],hi_in)[::-1]
    if g:return [1+lo[0]]+[lo[i]+hi[i-1] for i in range(1,len(p))]
    return [lo[i]+hi[i] for i in range(len(p))]

def bulk_step(p,g,lo_in,hi_in):
    lo=norm(p,lo_in);hi=norm(p[::-1],hi_in)[::-1]
    if g:return [lo[i]+hi[i-1] for i in range(1,len(p))]
    return [lo[i]+hi[i] for i in range(len(p))]

def centre_step(p,g,lo_in):
    d=norm(p,lo_in);n=len(d)
    if g:return [d[i+1]+d[n-1-i] for i in range(n-1)]
    return [d[i]+d[n-1-i] for i in range(n)]

def prefix_proof():
    p=[17-3*(i.bit_count()&1) for i in range(100)]
    gs=[];leading=[];odd=[]
    for t in range(10):
        leading.append(p[0])
        witness=next((i for i,x in enumerate(p) if x&1),None)
        assert witness is not None,(t,p)
        odd.append(witness)
        if t==9:break
        # By symmetry P[n-1]=P[0]. For P[0]!=9, overflow
        # is independent of the actual incoming final carry.
        assert p[0]!=9
        g=int(p[0]>=10);gs.append(g)
        outputs={tuple(prefix_step(p,g,hi)[:-2]) for hi in (0,1)}
        assert len(outputs)==1,(t,len(outputs))
        p=list(next(iter(outputs)))
    assert "".join(map(str,gs))=="101010101"
    assert len(p)==82 and [i for i,x in enumerate(p) if x==9]==[2]
    return {"p0_along_t0_to_t9":leading,"gamma":gs,
            "odd_witness_positions":odd,"final_prefix_length":82,
            "final_neutral_indices":[2]}

def bulk_proof(gs):
    W,n=factors(100)
    lo=100;hi=0
    for w in W:
        p=[17-3*int(z) for z in w]
        for t,g in enumerate(gs):
            # All FOUR entering-carry pairs, no unjustified
            # assumption on carry continuity through the window.
            outputs={tuple(bulk_step(p,g,a,b)[2:-2])
                     for a in (0,1) for b in (0,1)}
            assert len(outputs)==1,(w,t,len(outputs))
            p=list(next(iter(outputs)))
        assert len(p)==59 and 9 not in p,(w,p)
        lo=min(lo,min(p));hi=max(hi,max(p))
    assert len(W)==326 and n==512
    return {"factor_length":100,"factor_count":len(W),
            "closure_witness_substitution_length":n,
            "final_window_length":59,"all_carry_branches_collapse":True,
            "final_has_no_neutral_9":True,
            "min_final_coefficient":lo,"max_final_coefficient":hi}

def centre_proof(gs):
    W,n=factors(41);types={}
    for w in W:
        half=[17-3*int(z) for z in w]
        p=half+half[::-1]
        for t,g in enumerate(gs):
            outputs={tuple(centre_step(p,g,c)[2:-2]) for c in (0,1)}
            assert len(outputs)==1,(w,t,len(outputs))
            p=list(next(iter(outputs)))
        assert len(p)==41
        neutral=tuple(i-20 for i,x in enumerate(p) if x==9)
        suffix=w[-6:]
        assert neutral==((-1,1) if suffix in EXC else ()),(w,neutral)
        types.setdefault(suffix,set()).add(neutral)
    assert len(W)==128 and n==256 and len(types)==16
    assert all(len(z)==1 for z in types.values())
    return {"factor_length":41,"factor_count":len(W),
            "closure_witness_substitution_length":n,
            "centre_window_length_at_t9":41,"suffix_bits":6,
            "special_patterns":sorted(EXC),
            "nonspecial_factors":sum(w[-6:] not in EXC for w in W)}

def small_proof(gs):
    def tm(i):return i.bit_count()&1
    def source(k):
        n=2*k+8
        p=[17-3*tm(min(i,n-1-i)) for i in range(n)]
        d=[0]*n
        for i in range(n//2):
            h=min(9,p[i]);d[i]=p[i]-h;d[n-1-i]=h
        return d
    def step(d):
        out=[];c=0
        for x,y in zip(d,reversed(d)):
            z=x+y+c;out.append(z%10);c=z//10
        if c:out.append(c)
        return out
    def pw(d):return [d[i]+d[-i-1] for i in range(len(d))]
    for k in range(96):
        d=source(k);actual=[]
        for t in range(10):
            assert d!=d[::-1],(k,t)
            if t==9:break
            nd=step(d)
            v=int("".join(map(str,reversed(d))))
            assert v+int(str(v)[::-1])==int("".join(map(str,reversed(nd))))
            actual.append(len(nd)-len(d))
            d=nd
        assert actual==gs
        p=pw(d);n=len(p)
        assert n==2*k+13
        got={i for i,x in enumerate(p) if x==9}
        if k==0:want={2,10}
        elif k==1:want={2,4,6,8,10,12}
        else:
            bits="".join(str(tm(k+j)) for j in range(-2,4))
            want={2,n-3}
            if bits in EXC:want.update((k+5,k+7))
        assert got==want,(k,got,want)
    return {"widths_checked":96,"width_range":[0,95],
            "first_ten_states_nonpalindromic":True,
            "independent_bigint_edges":864,"exact_port_rule":True}

def density_proof():
    W=sorted(factors(6)[0]);assert len(W)==16
    double={"001011","010110","011001","011010",
            "100101","100110","101001","110100"}
    v=[2 if w in double else 1 for w in W]
    assert sum(v)==24
    M=[[0]*16 for _ in range(16)]
    for j,w in enumerate(W):
        s=sub(w)
        for z in (s[:6],s[1:7]):
            M[W.index(z)][j]+=1
    assert all(sum(M[i][j]*v[j] for j in range(16))==2*v[i]
               for i in range(16))
    B=[[bool(x) for x in row] for row in M]
    power=1
    while not all(all(row) for row in B) and power<=10:
        B=[[any(B[i][j] and M[j][k] for j in range(16))
            for k in range(16)] for i in range(16)]
        power+=1
    assert power==5 and all(all(row) for row in B)
    assert sum(v[W.index(w)] for w in EXC)==2
    return {"factor_length":6,"number_of_factors":16,
            "integer_stationary_weights":dict(zip(W,v)),
            "stationary_matrix_identity":"M*v=2*v",
            "first_strictly_positive_power":power,
            "exception_density":"1/12",
            "two_port_guard_density":"11/12"}

def main():
    a=prefix_proof()
    b=bulk_proof(a["gamma"])
    c=centre_proof(a["gamma"])
    d=small_proof(a["gamma"])
    e=density_proof()
    result={"status":"PAPER PROOF, finite exact checker + word-factor closure",
            "scope":"universal k>=0, exactly nine reverse-and-add steps, not infinite",
            "prefix":a,"bulk":b,"centre":c,"small":d,"density":e,
            "geometry":"k>=96: t9 lower-half prefix 0..81, bulk 23..(k+4-19), centre (k+4-18)..(k+4+2); all covered"}
    print(json.dumps(result,indent=2))
if __name__=="__main__":main()
