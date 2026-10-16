"""Literal integer audit of the new periodic-segment arithmetic.

These are implementation tests, not substitutes for an all-parameter proof.
No discovery-code numeric transition is used as the expected answer.
"""
import json,random
from math import lcm
from itertools import product
from astra_substitution_periodic import A,S,norm,reverse,step,digit_family,expand,safe,same,all_center_even,Unresolved

def realize(q,base):
    ds=[0]*len(q)
    for i in range(len(q)//2):
        ds[-1-i]=min(base-1,q[i]);ds[i]=q[i]-ds[-1-i]
    if len(q)%2:
        assert q[len(q)//2]%2==0;ds[len(q)//2]=q[len(q)//2]//2
    assert ds[-1]>0
    n=0
    for d in ds[::-1]:n=n*base+d
    return n

def numdigits(n,base):
    ds=[]
    while n:ds.append(n%base);n//=base
    return tuple(ds)

def reversed_number(n,base):
    r=0
    while n:r=base*r+n%base;n//=base
    return r

def numeric_center(q,k):
    lengths=[s.n.at(k) for s in q];total=sum(lengths)
    if total%2==0:return True
    i=total//2
    for s,n in zip(q,lengths):
        if i<n:return s.w[i%len(s.w)]%2==0
        i-=n
    raise AssertionError('missing center')

def audit():
    rng=random.Random(196);integer_checks=0;center_checks=0;branch_rejections=0
    for base in (2,3,10):
        for test in range(120):
            motifs=[tuple(rng.randrange(2*base-1) for _ in range(rng.randrange(1,5))) for j in range(3)]
            L=lcm(*(len(w) for w in motifs))
            half=[S((rng.randrange(1,2*base-1),),A(0,1))]
            half.extend(S(w,A(L*rng.randrange(1,4),len(w)*rng.randrange(8,20))) for w in motifs)
            q=norm(half+[S((2*rng.randrange(base),),A(0,1))]+list(reverse(half)))
            for t in range(5):
                try:d=digit_family(q,base);nxt=step(q,base)
                except Unresolved:branch_rejections+=1;break
                for k in (0,1,3,8):
                    raw=expand(q,k);n=realize(raw,base);out=n+reversed_number(n,base);ds=numdigits(out,base)
                    assert ds==expand(d,k)
                    assert tuple(a+b for a,b in zip(ds,ds[::-1]))==expand(nxt,k)
                    if safe(q,base):assert ds!=ds[::-1],(base,t,k,raw,ds)
                    integer_checks+=1
                q=nxt
    for test in range(1000):
        q=tuple(S(tuple(rng.randrange(19) for _ in range(rng.randrange(1,8))),A(rng.randrange(13),rng.randrange(1,61))) for j in range(rng.randrange(1,7)))
        bound=2*sum(s.n.b for s in q)+2*max(len(s.w) for s in q)
        samples=all(numeric_center(q,k) for k in range(bound+1))
        assert all_center_even(q)==samples,(q,bound,samples)
        center_checks+=1
    # The shortest member agrees, but a later periodic symbol disagrees.
    assert not same((S((0,1),A(2,1)),),(S((0,),A(2,1)),))
    # Simple local encoding controls use all-zero boundary bulks.
    from astra_substitution_gluing import query
    for kind in ('center','interface'):
        r=query(kind,(0,0,0),2,(0,0,0) if kind=='interface' else None,1)
        assert r['result']=='sat'
    # Independently realize all722 outer-prefix states with both possible
    # interior carries, so graph edges are checked with ordinary integers.
    from astra_substitution_enumerate import outer_three_filter,transition
    from astra_substitution_gluing import trace,cyclic
    from astra_substitution_twobulk import pool
    graph=outer_three_filter();prefix_checks=0
    for row in graph['graph']:
        q=tuple(row['q']);expected=set()
        for carry in (0,1):
            full=q+(18*carry,)+q[::-1]
            number=realize(full,10);ds=numdigits(number+reversed_number(number,10),10)
            new=tuple(a+b for a,b in zip(ds,ds[::-1]));head=new[:3]
            if head[0]==(17 if q[0]==8 else 8):expected.add(head)
            prefix_checks+=1
        assert expected==set(map(tuple,row['targets']))
    # All28 positive center loops are checked at every phase inside literal
    # finite symmetric decimal words padded by four periods of the bulk.
    direct_motifs=[]
    for initial in product(range(19),repeat=3):
        if len(set(initial))==1:continue
        current=initial
        for t in range(24):
            if all(v==9 for v in current):break
            data=cyclic(current)
            current=tuple(data['lo'][i]+data['hi'][(i-t%2)%3] for i in range(3))
        else:
            if current==initial:direct_motifs.append(initial)
    assert sorted(direct_motifs)==pool(24)
    center_integer_checks=0;certificates=[]
    rows=json.load(open('astra_substitution_center_enumeration.json'))
    for row in rows:
        if not row['return_loops']:continue
        bt=trace(tuple(row['B']));w=tuple(row['samples'][0]);phases=[]
        for t in range(24):
            g=t//2;d=g//2;shift=((t+1)//2)//2-d
            phases.append({'t':t,'overflow':t%2,'bulk':bt[t]['q'],'center':w,'center_start_shift':d,'left_carry_in':bt[t]['A'][d%3],'left_carry_out':bt[t]['R'][d%3]})
            q=bt[t]['q'];left=(8 if t%2==0 else 18,)+tuple(q[i%3] for i in range(12+d))
            full=left+w+left[::-1];number=realize(full,10)
            ds=numdigits(number+reversed_number(number,10),10)
            raw=tuple(a+b for a,b in zip(ds,ds[::-1]))
            nxt=transition('center',w,bt,t);assert nxt is not None
            begin=len(left)+shift
            assert raw[begin:begin+len(nxt)]==nxt
            w=nxt;center_integer_checks+=1
        assert w==tuple(row['samples'][0])
        certificates.append({'bulk':row['B'],'initial_center':row['samples'][0],'period':24,'total_center_start_shift':6,'phases':phases,'scope':'Exact local center component; requires compatible finite exterior/interface.'})
    open('astra_substitution_center_certificates.json','w').write(json.dumps(certificates,indent=2)+'\n')
    return dict(literal_integer_comparisons=integer_checks,exact_center_family_cases=center_checks,conservative_branch_rejections=branch_rejections,latent_period_mismatch_control=True,local_zero_bulk_controls=True,outer_graph_literal_integer_cases=prefix_checks,positive_center_phase_integer_checks=center_integer_checks,direct_nonneutral_bulk_words_enumerated=19**3-19,direct_returning_nonconstant_motifs=len(direct_motifs))

if __name__=='__main__':
    result=audit();open('astra_substitution_audit_results.json','w').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
