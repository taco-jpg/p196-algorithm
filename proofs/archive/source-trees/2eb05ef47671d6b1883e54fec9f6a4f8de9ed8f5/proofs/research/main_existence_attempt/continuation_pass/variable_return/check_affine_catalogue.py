"""Independent all-parameter replay without the affine run normalizer.

Uses sparse (x-1)-multiplied run polynomials, adapting the independently
audited renewal_pass/tails/check_symbolic_tails.py method. Also redoes
every target equality as a complete system of affine length equations.
"""
from collections import defaultdict, Counter
import gzip
import hashlib
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent


def plus(a,b):
    return a[0]+b[0],a[1]+b[1]


def clean(p):
    return {e:c for e,c in p.items() if c}


def add(*polys):
    p=defaultdict(int)
    for a in polys:
        for e,c in a.items():
            p[e]+=c
    return clean(p)


def numerator(runs,carry=False):
    p=defaultdict(int)
    position=(0,0)
    c=0
    for symbol,coeff,constant in runs:
        assert len(coeff)==1 and coeff[0]>=0 and constant>0
        end=plus(position,(coeff[0],constant))
        if carry:
            first=(symbol+c)//10
            assert first in (0,1) and (symbol+first)//10==first
            assert 0<=(symbol+c)%10<=9 and 0<=(symbol+first)%10<=9
            c=first
            value=c
        else:
            value=symbol
        p[end]+=value
        p[position]-=value
        position=end
    return clean(p),position,c


def reflect(poly,width):
    return {(width[0]-e[0],width[1]-e[1]):-c for e,c in poly.items()}


def canonical_rle(runs):
    out=[]
    for symbol,a,b in runs:
        if out and out[-1][0]==symbol:
            out[-1][1][0]+=a[0]
            out[-1][2]+=b
        else:
            out.append([symbol,[a[0]],b])
    return out


def start(case,base):
    p,u,v=case
    return canonical_rle([[p,[0],2],[0,[1],base-1],[u,[0],1],
                          [u+v,[0],1],[2*v,[0],1],[u+v,[0],1],
                          [u,[0],1],[0,[1],base-1],[p,[0],2]])


def equality(left,right):
    if [s for s,_,_ in left]!=[s for s,_,_ in right]:
        return 'different symbols'
    root=None
    for (_,a,b),(_,c,d) in zip(left,right):
        slope=a[0]-c[0]
        constant=b-d
        if not slope:
            if constant:
                return {'constant_mismatch':constant}
        else:
            if (-constant)%slope:
                return {'noninteger_root':[slope,constant]}
            k=(-constant)//slope
            if k<0 or (root is not None and root!=k):
                return {'incompatible_root':k,'prior':root}
            root=k
    return {'MATCH': 'ALL' if root is None else root}


def main():
    meta=json.loads((HERE/'affine_catalogue.json').read_text())
    raw=gzip.decompress((HERE/meta['archive']['path']).read_bytes())
    assert hashlib.sha256(raw).hexdigest()==meta['archive']['sha256']
    rows=json.loads(raw)
    catalogue=[tuple(c) for c in meta['catalogue']]
    assert len(catalogue)==180 and len(set(catalogue))==180
    previous={c:start(c,40) for c in catalogue}
    targets={c:start(c,41) for c in catalogue}
    clocks={c:[] for c in catalogue}
    safety={c:True for c in catalogue}
    mismatches=Counter()
    compatible=[]
    checked=0
    for row in rows:
        case=tuple(row['case'])
        q=previous[case]
        out=row['q']
        Q,L,_=numerator(q)
        assert Q==reflect(Q,L) and q[0][0]>0
        assert all(0<=s<=18 for s,_,_ in q+out)
        C,CL,h=numerator(q,carry=True)
        assert CL==L
        D=add(Q,{plus(e,(0,1)):v for e,v in C.items()},
              {e:-10*v for e,v in C.items()})
        W=plus(L,(0,h))
        O,OW,_=numerator(out)
        assert OW==W and O==add(D,reflect(D,W))
        assert O==reflect(O,W) and out[0][0]>0
        assert canonical_rle(out)==out
        clocks[case].append(h)
        assert row['time']==len(clocks[case]) and row['clock']==clocks[case]
        present={s for s,_,_ in q}
        safety[case] &= not (max(present)<=9 or (q[0][0]==11 and present<={0,11}))
        assert row['safe_through']==safety[case]
        for target,z in targets.items():
            result=equality(out,z)
            assert not (isinstance(result,dict) and 'MATCH' in result), (row,target,result)
            if result=='different symbols':
                mismatches['different_symbols']+=1
            else:
                mismatches['affine_length_mismatch']+=1
                compatible.append({'input':case,'time':row['time'],'target':target,
                                   'witness':result})
        previous[case]=out
        checked+=1
    assert all(len(v)==12 for v in clocks.values())
    assert checked==2160
    controls_raw=gzip.decompress((HERE/meta['integer_control_archive']['path']).read_bytes())
    assert hashlib.sha256(controls_raw).hexdigest()==meta['integer_control_archive']['sha256']
    integer_records=json.loads(controls_raw)
    integer_steps=0
    small_targets={}
    for r in range(1,40):
        small_targets[r]=set()
        for p,u,v in catalogue:
            small_targets[r].add((p,p)+(0,)*r+(u,u+v,2*v,u+v,u)+(0,)*r+(p,p))
    covered=set()
    for record in integer_records:
        case=tuple(record['case']);r=record['r']
        covered.add((case,r))
        values=list(map(int,record['integers']))
        assert len(values)==13
        p,u,v=case
        initial=(p,p)+(0,)*(r-1)+(u,u+v,2*v,u+v,u)+(0,)*(r-1)+(p,p)
        s=str(values[0]);actual=tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))
        assert actual==initial
        for a,b in zip(values,values[1:]):
            assert b==a+int(str(a)[::-1])
            s=str(b);q=tuple(int(x)+int(y) for x,y in zip(s,s[::-1]))
            if r<40:
                assert q not in small_targets[r]
            integer_steps+=1
    assert len(covered)==180*43 and integer_steps==92880
    assert all((case,r) in covered for case in catalogue for r in range(1,40))
    # Independently verify every one-step potential inequality used to turn
    # the finite time window into an all-positive-time exclusion.
    psi=(0,4,3,2,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0)
    edges=[]
    for a in range(1,19):
        for b in (0,1):
            h=(a+b)//10
            z=2*a+b if not h else a+1-10*(a//10)
            slack=psi[a]+4*h-psi[z]-1
            assert slack>=0
            edges.append({'outer':a,'incoming':b,'overflow':h,'next_outer':z,'slack':slack})
    result={'status':'PASS','symbolic_transition_count':checked,
            'complete_target_comparisons':sum(mismatches.values()),
            'comparison_counts':dict(mismatches),'symbol_compatible_exclusions':compatible,
            'potential_edges':edges,'imports_generator_or_run_normalizer':False,
            'uses_parameter_samples_as_proof':False,'formalized_in_Lean':False,
            'archive_sha256':hashlib.sha256(raw).hexdigest(),
            'integer_control_payload_sha256':hashlib.sha256(controls_raw).hexdigest(),
            'ordinary_integer_transitions_replayed':integer_steps,
            'scope':'all r>=40 symbolic transitions/exclusions, all small r=1..39 integer transitions/exclusions, and exact all-time potential bound',
            'decimal_lychrel_existence_proved':False}
    (HERE/'affine_catalogue_audit.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='potential_edges'},indent=2))


if __name__=='__main__':
    main()
