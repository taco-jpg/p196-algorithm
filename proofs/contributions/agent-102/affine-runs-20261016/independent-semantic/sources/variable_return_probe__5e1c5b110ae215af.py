"""Exact bounded-catalogue reset tests, with explicitly separate scopes.

1. All spacers r>=1, all return times, target spacer r+1, and the 180
   generalized overlap templates: exact affine arithmetic plus all small r.
2. Multiplicative spacer targets 2r-1, 2r, 2r+1 for r=3..32: finite
   ordinary-integer search, continued through palindromes, with all outcomes.

No capped trajectory is represented as an infinite construction.
"""
from __future__ import annotations

from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "main_existence_attempt/smart_pass/collision"))
import orthant_runs as run

HERE = Path(__file__).resolve().parent
BASE = 40
ONE = run.Length((0,), 1)
GAP = run.Length((1,), BASE)
PSI = (0,4,3,2,2,2,1,1,1,1,1,0,0,0,0,0,0,0,0)


def cores():
    out = []
    for u in range(1, 4):
        for v in range(5, 8):
            if u+v <= 8:
                out.append((u,v))
    for u in range(5, 9):
        for v in (5,6):
            if u+v <= 13:
                out.append((u,v))
    for u in range(10,14):
        for v in (5,6):
            if u+v <= 18:
                out.append((u,v))
    assert len(out) == 20
    return out


CATALOGUE = tuple((p,u,v) for p in range(1,10) for u,v in cores())


def family(p,u,v, gap=GAP):
    # Q=(1+x)[p 0^r (u,v,v,u) 0^r p].
    return run.canon([(p,run.Length((0,),2)), (0,gap-ONE),
                      (u,ONE),(u+v,ONE),(2*v,ONE),(u+v,ONE),(u,ONE),
                      (0,gap-ONE),(p,run.Length((0,),2))])


def literal_family(p,u,v,r):
    return (p,p)+(0,)*(r-1)+(u,u+v,2*v,u+v,u)+(0,)*(r-1)+(p,p)


def canonical(q):
    return (q and q[0]>0 and q==q[::-1] and all(0<=x<=18 for x in q)
            and (len(q)%2==0 or q[len(q)//2]%2==0))


def realize(q):
    assert canonical(q)
    digits=[0]*len(q)
    for i in range(len(q)//2):
        digits[i]=max(0,q[i]-9)
        digits[-i-1]=min(9,q[i])
    if len(q)%2:
        digits[len(q)//2]=q[len(q)//2]//2
    return int(''.join(map(str,digits[::-1])))


def qword(n):
    s=str(n)
    return tuple(int(a)+int(b) for a,b in zip(s,s[::-1]))


def next_number(n):
    return n+int(str(n)[::-1])


def safe(q):
    present=[a for a,_ in q]
    return not (max(present)<=9 or (present[0]==11 and set(present)<={0,11}))


def equal_parameters(left,right):
    """Return ALL, NONE, or the unique k>=0 where these positive RLEs agree.

    All run lengths are positive for every k>=0. RLE uniqueness therefore
    reduces equality to the exact affine equations, including isolated roots.
    """
    assert all(n.positive() for _,n in left+right)
    if tuple(x for x,_ in left)!=tuple(x for x,_ in right):
        return "NONE"
    root=None
    for (_,a),(_,b) in zip(left,right):
        slope=a.coefficients[0]-b.coefficients[0]
        constant=a.constant-b.constant
        if slope==0:
            if constant:
                return "NONE"
        else:
            if (-constant)%slope:
                return "NONE"
            candidate=(-constant)//slope
            if candidate<0 or (root is not None and candidate!=root):
                return "NONE"
            root=candidate
    return "ALL" if root is None else root


def compressed_json(path,value):
    raw=json.dumps(value,sort_keys=True,separators=(',',':')).encode()
    with path.open('wb') as f:
        with gzip.GzipFile(fileobj=f,mode='wb',mtime=0) as g:
            g.write(raw)
    return {'path':path.name,'records':len(value),'sha256':hashlib.sha256(raw).hexdigest(),
            'compressed_sha256':hashlib.sha256(path.read_bytes()).hexdigest()}


def affine_catalogue():
    """All r, all t, with target r+1 and any target in the catalogue.

    Width increment is two. The existing exact potential gives t<=12
    regardless of the two outer symbols. No fixed overflow clock is used.
    """
    targets=defaultdict(list)
    for target in CATALOGUE:
        w=family(*target,gap=GAP+ONE)
        targets[tuple(x for x,_ in w)].append((target,w))
    all_rows=[]
    integer_records=[]
    matches=[]
    controls=0
    affine_transitions=0
    full_comparisons=0
    for case in CATALOGUE:
        w=family(*case)
        safety=True
        clocks=[]
        for t in range(1,13):
            safety &= safe(w)
            w,h=run.step(w)
            affine_transitions+=1
            clocks.append(h)
            row={'case':case,'time':t,'q':run.as_json(w),'clock':clocks.copy(),
                 'safe_through':safety,'matches':[]}
            for target,z in targets.get(tuple(x for x,_ in w),[]):
                full_comparisons+=1
                eq=equal_parameters(w,z)
                if eq!='NONE':
                    # Sharper phase-dependent bound than the global 12.
                    assert t<=8+PSI[case[0]]-PSI[target[0]]
                    item={'case':case,'target':target,'time':t,'parameters':eq,
                          'safe_through':safety}
                    matches.append(item)
                    row['matches'].append(item)
            all_rows.append(row)
        for r in range(1,BASE):
            n=realize(literal_family(*case,r))
            integers=[str(n)]
            target_dict={literal_family(*target,r+1):target for target in CATALOGUE}
            first_pal=None
            for t in range(1,13):
                n=next_number(n)
                integers.append(str(n))
                controls+=1
                if first_pal is None and str(n)==str(n)[::-1]:
                    first_pal=t
                q=qword(n)
                if q in target_dict:
                    target=target_dict[q]
                    assert t<=8+PSI[case[0]]-PSI[target[0]]
                    matches.append({'case':case,'target':target,'time':t,
                                    'r':r,'safe_through':first_pal is None})
            integer_records.append({'case':case,'r':r,'kind':'complete_small_boundary',
                                    'integers':integers,'first_palindrome':first_pal})
        # Independent literal samples of the symbolic trajectories, including
        # a long spacer. These do not replace the symbolic proof.
        for k in (0,1,17,256):
            n=realize(literal_family(*case,BASE+k))
            integers=[str(n)]
            for row in all_rows[-12:]:
                n=next_number(n)
                integers.append(str(n))
                controls+=1
                qq=tuple(x for x,coeff,c in row['q'] for _ in range(coeff[0]*k+c))
                assert qword(n)==qq
            integer_records.append({'case':case,'r':BASE+k,'kind':'symbolic_identity_control',
                                    'integers':integers})
    archive=compressed_json(HERE/'affine_catalogue_outcomes.json.gz',all_rows)
    integer_archive=compressed_json(HERE/'affine_literal_controls.json.gz',integer_records)
    result={'status':'complete in the stated catalogue, all r>=1 and all positive return times',
            'catalogue':CATALOGUE,'target_spacer':'r+1','affine_domain':f'r={BASE}+k, k>=0',
            'small_spacers':f'1..{BASE-1}','return_time_bound':12,
            'fixed_clock':False,'affine_transitions':affine_transitions,
            'symbol-compatible_affine_comparisons':full_comparisons,
            'symbol_incompatible_comparisons':affine_transitions*len(CATALOGUE)-full_comparisons,
            'independent_integer_transitions':controls,'all_matches':matches,
            'archive':archive,'all_time_avoidance_proved':False}
    result['integer_control_archive']=integer_archive
    (HERE/'affine_catalogue.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k not in ('catalogue','all_matches') } | {'matches':len(matches)}


def multiplicative_catalogue():
    rows=[]
    matches=[]
    total_steps=0
    started=time.monotonic()
    for case in CATALOGUE:
        for r in range(3,33):
            target_rs=(2*r-1,2*r,2*r+1)
            targets={literal_family(*target,rr):(target,rr)
                     for target in CATALOGUE for rr in target_rs}
            target_widths={2*rr+7 for rr in target_rs}
            width_limit=max(target_widths)
            n=realize(literal_family(*case,r))
            initial=n
            first_pal=None
            clocks=[]
            hits=[]
            digest=hashlib.sha256()
            t=0
            # Stop only after passing the largest target width. Width cannot
            # decrease. The exact growth potential proves this loop terminates.
            while len(str(n))<=width_limit:
                old_width=len(str(n))
                n=next_number(n)
                t+=1
                total_steps+=1
                s=str(n)
                clocks.append(len(s)-old_width)
                digest.update(s.encode()+b'\n')
                if first_pal is None and s==s[::-1]:
                    first_pal=t
                if len(s) in target_widths:
                    q=qword(n)
                    if q in targets:
                        target,rr=targets[q]
                        item={'case':case,'r':r,'target':target,'target_r':rr,
                              'time':t,'first_palindrome':first_pal,
                              'safe_through':first_pal is None}
                        hits.append(item)
                        matches.append(item)
            # One final update leaves the largest possible target width.
            assert t<=4*(len(str(n))-len(str(initial)))+PSI[case[0]]
            rows.append({'case':case,'r':r,'target_rs':target_rs,
                         'seed':str(initial),'checked_steps':t,
                         'last_width':len(str(n)),'last_integer':str(n),
                         'first_palindrome':first_pal,'clock':''.join(map(str,clocks)),
                         'trajectory_sha256':digest.hexdigest(),'matches':hits,
                         'status':'complete for these three target spacers'})
    archive=compressed_json(HERE/'multiplicative_catalogue_outcomes.json.gz',rows)
    result={'status':'finite seed-parameter classification; no all-r or infinite conclusion',
            'catalogue_size':len(CATALOGUE),'initial_r':'3..32',
            'target_r':['2r-1','2r','2r+1'],'input_cases':len(rows),
            'ordinary_integer_steps':total_steps,'caps':None,
            'stop_rule':'first state wider than every target; exact width monotonicity',
            'all_matches':matches,'archive':archive,'seconds':time.monotonic()-started,
            'all_time_avoidance_proved':False}
    (HERE/'multiplicative_catalogue.json').write_text(json.dumps(result,indent=2)+'\n')
    return {k:v for k,v in result.items() if k!='all_matches'} | {'matches':len(matches)}


if __name__=='__main__':
    print(json.dumps(affine_catalogue(),indent=2),flush=True)
    print(json.dumps(multiplicative_catalogue(),indent=2),flush=True)
