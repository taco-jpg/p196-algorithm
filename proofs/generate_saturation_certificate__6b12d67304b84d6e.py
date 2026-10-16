#!/usr/bin/env python3
"""Reproduce the exact accepted Lean saturation certificate using only Python.

Graph algorithms discover a rank; every control is then proved separately by the
Lean kernel. No graph algorithm or Python result is an axiom of the theorem.
"""
from __future__ import annotations
import hashlib
import json
from collections import deque
from itertools import product
from pathlib import Path
from complementary_bulk import direct_pair, pair, realize

ROOT = Path(__file__).resolve().parent
UP = (0,0,0,0,1,0,1,1,1,2,1,1,1,2,1,2,2,2,3)
CYCLE = ((8,14,8),(17,8,17),(8,16,16),(17,13,14),(8,12,9),(17,5,0),(8,13,5),(17,6,11))
EXPECTED_DATA = '5b0226596896f5abada85ccb7b39803c7e1bf7f5e02364276e576bfc6e83d3c0'


def transition(q: tuple[int,int,int], e: int) -> tuple[tuple[int,int,int],int]:
    p,a,b=q
    l1=p//10; l2=(a+l1)//10
    r2=(b+e)//10; r1=(a+r2)//10; gamma=(p+r1)//10
    left=(p%10,(a+l1)%10,(b+l2)%10)
    right=((p+r1)%10,(a+r2)%10,(b+e)%10)
    out=(left[0]+1,left[1]+right[0],left[2]+right[1]) if gamma else tuple(x+y for x,y in zip(left,right))
    return out,gamma


def components(adj: list[set[int]]) -> tuple[list[list[int]],list[int]]:
    """Iterative Kosaraju; no recursion-depth or external dependency."""
    seen=set();order=[]
    reverse=[set() for _ in adj]
    for u,vs in enumerate(adj):
        for v in vs: reverse[v].add(u)
    for root in range(len(adj)):
        if root in seen: continue
        seen.add(root); stack=[(root,iter(sorted(adj[root])))]
        while stack:
            u,it=stack[-1]
            v=next(it,None)
            if v is None:
                stack.pop();order.append(u)
            elif v not in seen:
                seen.add(v);stack.append((v,iter(sorted(adj[v]))))
    group=[-1]*len(adj);parts=[]
    for root in reversed(order):
        if group[root]>=0: continue
        k=len(parts);part=[];stack=[root];group[root]=k
        while stack:
            u=stack.pop();part.append(u)
            for v in reverse[u]:
                if group[v]<0: group[v]=k;stack.append(v)
        parts.append(part)
    return parts,group


def main() -> None:
    states=[(p,a,b) for p in range(1,19) for a,b in product(range(19),repeat=2)]
    index={q:i for i,q in enumerate(states)}
    adj=[set() for _ in states];controls=[];digest=hashlib.sha256()
    for u,q in enumerate(states):
        for e in (0,1):
            out,g=transition(q,e);v=index[out]
            slack=1+UP[q[0]]-UP[out[0]]-2*g
            assert g in (0,1) and slack>=0
            word=q+(18*e,18*e)+q[::-1]
            assert direct_pair(word)[:3]==out
            n=realize(word);result=n+int(str(n)[::-1])
            digits=tuple(map(int,str(result)[::-1]))
            assert pair(digits)[:3]==out and len(digits)==len(word)+g
            digest.update(json.dumps([q,e,out,g,result],separators=(',',':')).encode()+b'\n')
            controls.append((u,v,e,g,slack))
            if slack==0: adj[u].add(v)
    parts,group=components(adj)
    cyclic=[part for part in parts if len(part)>1 or part[0] in adj[part[0]]]
    assert len(cyclic)==1 and {states[u] for u in cyclic[0]}==set(CYCLE)
    core={index[q] for q in CYCLE}
    assert {(states[u],states[v]) for u in core for v in adj[u] if v in core}==set(zip(CYCLE,CYCLE[1:]+CYCLE[:1]))
    dag=[set() for _ in parts]
    for u,vs in enumerate(adj):
        for v in vs:
            if group[u]!=group[v]: dag[group[u]].add(group[v])
    incoming=[0]*len(parts)
    for vs in dag:
        for v in vs: incoming[v]+=1
    ready=deque(i for i,d in enumerate(incoming) if d==0);order=[]
    while ready:
        u=ready.popleft();order.append(u)
        for v in dag[u]:
            incoming[v]-=1
            if incoming[v]==0: ready.append(v)
    assert len(order)==len(parts)
    heights=[0]*len(parts)
    for u in reversed(order): heights[u]=max((heights[v]+1 for v in dag[u]),default=0)
    ranks=[heights[group[u]] for u in range(len(states))];phases={q:i for i,q in enumerate(CYCLE)}
    for u,v,e,g,slack in controls:
        if slack==0:
            assert ranks[v]<=ranks[u]
            if ranks[v]==ranks[u]: assert phases[states[v]]==(phases[states[u]]+1)%8
    source='''import PeriodObstructions

namespace Agent8.Saturation

abbrev Triple := Nat × Nat × Nat

def next (q : Triple) (e : Nat) : Triple :=
  let p := q.1
  let a := q.2.1
  let b := q.2.2
  let l1 := p / 10
  let l2 := (a + l1) / 10
  let r2 := (b + e) / 10
  let r1 := (a + r2) / 10
  let g := (p + r1) / 10
  if g = 0 then
    (p % 10 + (p+r1) % 10,
      (a+l1) % 10 + (a+r2) % 10,
      (b+l2) % 10 + (b+e) % 10)
  else
    (p % 10 + 1,
      (a+l1) % 10 + (p+r1) % 10,
      (b+l2) % 10 + (a+r2) % 10)

def overflow3 (q : Triple) (e : Nat) : Nat :=
  (q.1 + (q.2.1 + (q.2.2 + e)/10)/10)/10

def valid (q : Triple) : Prop :=
  0 < q.1 ∧ q.1 ≤ 18 ∧ q.2.1 ≤ 18 ∧ q.2.2 ≤ 18

def packedRow (p a : Nat) : Nat :=
  match p with
'''
    for p in range(1,19):
        source+=f'  | {p} => match a with\n'
        for a in range(19):
            values=[ranks[index[(p,a,b)]] for b in range(19)]
            assert max(values)<64
            packed=sum(v*64**b for b,v in enumerate(values))
            assert all((packed//64**b)%64==v for b,v in enumerate(values))
            source+=f'    | {a} => {packed}\n'
        source+='    | _ => 0\n'
    source+='''  | _ => 0

def rank (q : Triple) : Nat :=
  (packedRow q.1 q.2.1 / 64^q.2.2) % 64

def phase : Triple → Nat
'''
    source+=''.join(f'  | ({p}, {a}, {b}) => {i}\n' for i,(p,a,b) in enumerate(CYCLE))
    source+='''  | _ => 0

def slack (q : Triple) (e : Nat) : Int :=
  1 + upperPotential q.1 - upperPotential (next q e).1 - 2*(overflow3 q e : Int)

def Certificate (q : Triple) (e : Nat) : Prop :=
  valid (next q e) ∧ 0 ≤ slack q e ∧
    (slack q e = 0 → rank (next q e) ≤ rank q ∧
      (rank (next q e) = rank q → phase (next q e) = (phase q+1)%8))

end Agent8.Saturation
'''
    assert hashlib.sha256(source.encode()).hexdigest()==EXPECTED_DATA
    files={'SaturationData.lean':source}
    for p in range(1,19):
        files[f'SaturationShard{p}.lean']=f'''import SaturationData

namespace Agent8.Saturation

set_option maxRecDepth 10000 in
set_option maxHeartbeats 0 in
theorem certificate_{p} :
    ∀ a b : Fin 19, ∀ e : Fin 2, Certificate ({p},a.val,b.val) e.val := by
  unfold Certificate valid
  decide +kernel

#print axioms certificate_{p}

end Agent8.Saturation
'''
    wrapper=''.join(f'import SaturationShard{p}\n' for p in range(1,19))
    wrapper+='''
namespace Agent8.Saturation

theorem finite_certificate :
    ∀ p : Fin 18, ∀ a b : Fin 19, ∀ e : Fin 2,
      Certificate (p.val+1,a.val,b.val) e.val := by
  intro p a b e
  have hp : '''+' ∨ '.join(f'p.val = {p}' for p in range(18))+' := by omega\n'
    wrapper+='  rcases hp with '+' | '.join('h' for _ in range(18))+'\n'
    wrapper+=''.join(f'  · simpa only [h] using certificate_{p} a b e\n' for p in range(1,19))
    wrapper+='\n#print axioms finite_certificate\n\nend Agent8.Saturation\n'
    files['SaturationCertificate.lean']=wrapper
    manifest={}
    for name,text in files.items():
        (ROOT/name).write_text(text)
        manifest[name]={'bytes':len(text.encode()),'sha256':hashlib.sha256(text.encode()).hexdigest()}
    (ROOT/'saturation-generated-manifest.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    summary={'states':len(states),'controls':len(controls),'tight_edges':sum(map(len,adj)),
        'cyclic_components':len(cyclic),'cycle':CYCLE,'max_rank':max(ranks),
        'core_rank':ranks[index[CYCLE[0]]],'literal_integer_controls':len(controls),
        'control_stream_sha256':digest.hexdigest(),'data_sha256':EXPECTED_DATA,
        'scope':'exact discovery and input replay; compile the generated Lean files for proof'}
    (ROOT/'saturation-controls.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    print(json.dumps(summary,sort_keys=True))


if __name__=='__main__': main()
