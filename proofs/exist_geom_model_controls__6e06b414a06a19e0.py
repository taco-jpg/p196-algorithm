"""Independent ordinary-integer controls for the two exact pump models."""
import json,random
from pathlib import Path
from exist_geom_periodic_qpump import realize,numeric_q


def periodic_controls():
    rng=random.Random(20261013)
    checked={0:0,1:0};rejected={'boundary_carry':0,'high_absorption':0}
    for trial in range(20000):
        k=rng.randrange(1,17);r=4;m=3
        u,v=rng.randrange(19),rng.randrange(19);Q=[u,v,v,u]
        E=[rng.randrange(19) for _ in range(k)];E[0]=rng.randrange(1,19)
        full=E+Q*(2*m)+E[::-1];n=realize(full)
        carries=[0];digits=[]
        for q in full:
            total=q+carries[-1];digits.append(total%10);carries.append(total//10)
        h=carries[-1]
        A=[carries[k+2*r+j] for j in range(r)]
        B=[carries[len(full)-k-2*r-j] for j in range(r)]
        assert all(A[(j+1)%r]==(Q[j]+A[j])//10 for j in range(r))
        assert all(B[j]==(Q[j]+B[(j+1)%r])//10 for j in range(r))
        if carries[k]!=A[0] or carries[len(full)-k]!=B[0]:
            rejected['boundary_carry']+=1;continue
        lo=[(Q[j]+A[j])%10 for j in range(r)]
        hi=[(Q[j]+B[(j+1)%r])%10 for j in range(r)]
        eh=[digits[len(full)-1-i] for i in range(k)]
        if h and eh[-1]!=hi[-1]:
            rejected['high_absorption']+=1;continue
        el=digits[:k]
        EE=[el[i]+(1 if i==0 else eh[i-1]) for i in range(k)] if h else [el[i]+eh[i] for i in range(k)]
        QQ=[lo[j]+hi[(j-1)%r] for j in range(r)] if h else [lo[j]+hi[j] for j in range(r)]
        expected=EE+[QQ[j%r] for j in range(2*r*m+h)]+EE[::-1]
        nn=n+int(str(n)[::-1]);assert numeric_q(nn)==expected
        assert expected==expected[::-1]
        if len(expected)%2:assert expected[len(expected)//2]%2==0
        checked[h]+=1
    return {'sampled':20000,'accepted_exact_steps':checked,
            'not_in_fixed_cut_class':rejected}


def uniform_controls():
    rng=random.Random(2026101301);counts={0:0,1:0}
    for _ in range(100000):
        k=rng.randrange(1,10);M=10**k;d=rng.randrange(1,10)
        A=rng.randrange(M//10,M);B=rng.randrange(M)
        rev=lambda v:int(str(v).zfill(k)[::-1])
        eps=int(d>=5);dd=2*d-9*eps
        low=B+rev(A)
        if low//M!=eps:continue
        high=A+rev(B)+eps;h=high//M
        if h and high%10!=dd:continue
        aa=high//10 if h else high;bb=low%M
        for m in [1,2,11]:
            n=int(str(A)+str(d)*m+str(B).zfill(k))
            nn=n+int(str(n)[::-1])
            expected=str(aa)+str(dd)*(m+h)+str(bb).zfill(k)
            assert str(nn)==expected
        counts[h]+=1
    return {'sampled':100000,'accepted_exact_steps':counts,
            'bulk_lengths_tested_per_step':[1,2,11]}


if __name__=='__main__':
    result={'periodic_q':periodic_controls(),'uniform_digits':uniform_controls(),
            'scope':'Finite implementation controls, not infinite-existence certificates.'}
    Path('exist_geom_model_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))
