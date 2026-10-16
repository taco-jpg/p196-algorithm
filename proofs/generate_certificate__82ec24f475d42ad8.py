"""Produce a kernel-checkable certificate for every three-column exterior edge.

No graph library or floating-point optimization is used by this producer.
Its output is accepted only after Lean's kernel checks every finite edge.
"""
from __future__ import annotations
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path

U=(0,0,0,0,1,0,1,1,1,2,1,1,1,2,1,2,2,2,3)
CRITICAL=((8,12,9),(17,5,0),(8,13,5),(17,6,11),
          (8,14,8),(17,8,17),(8,16,16),(17,13,14))


def step(p: tuple[int,int,int], incoming: int):
    high=[]
    carry=incoming
    for q in reversed(p):
        carry,d=divmod(q+carry,10)
        high.append(d)
    gamma=carry
    high.reverse()
    low=[]
    carry=0
    for q in p:
        carry,d=divmod(q+carry,10)
        low.append(d)
    aligned=high if gamma==0 else [1]+high[:-1]
    return tuple(a+b for a,b in zip(low,aligned)),gamma


def generate(folder: Path):
    vertices=[(a,b,c) for a in range(1,19) for b in range(19) for c in range(19)]
    index={s:i for i,s in enumerate(vertices)}
    clock={s:i for i,s in enumerate(CRITICAL)}
    edges=[]
    tight=[]
    for i,v in enumerate(vertices):
        for e in (0,1):
            w,g=step(v,e)
            j=index[w]
            assert g in (0,1)
            assert 2*g+U[w[0]]<=1+U[v[0]]
            edges.append((i,j,g,e))
            if 2*g+U[w[0]]==1+U[v[0]]:
                critical=v in clock and w in clock and clock[w]==(clock[v]+1)%8
                tight.append((i,j,0 if critical else 1))
    # Longest-path certificate with the eight recurrent edges assigned cost 0.
    # A positive-cost cycle would prevent convergence and abort the producer.
    rank=[0]*len(vertices)
    for _ in range(len(vertices)+1):
        changed=False
        for i,j,cost in tight:
            bound=rank[j]+cost
            if rank[i]<bound:
                rank[i]=bound
                changed=True
        if not changed:
            break
    else:
        raise RuntimeError('No finite strictness certificate was produced')
    K=max(rank)+1
    assert K==41
    potential=[K*U[s[0]]+rank[i] for i,s in enumerate(vertices)]
    edge_digest=sha256()
    tight_count=0
    for i,j,g,e in edges:
        slack=K+potential[i]-2*K*g-potential[j]
        assert slack>=0
        if slack==0:
            tight_count+=1
            assert vertices[i] in clock and vertices[j] in clock
            assert clock[vertices[j]]==(clock[vertices[i]]+1)%8
        edge_digest.update((json.dumps([vertices[i],e,vertices[j],g,
            potential[i],potential[j]],separators=(',',':'))+'\n').encode())
    funcs=[]
    for a in range(1,19):
        groups={}
        for b in range(19):
            seq=[potential[index[(a,b,c)]] for c in range(19)]
            runs=[]
            for c,val in enumerate(seq):
                if c==0 or val!=seq[c-1]:
                    runs.append([c,c,val])
                else:
                    runs[-1][1]=c
            expression=str(runs[-1][2])
            for lo,hi,val in reversed(runs[:-1]):
                expression=f'if c ≤ {hi} then {val} else ({expression})'
            groups.setdefault(expression,[]).append(b)
        body='\n'.join('  | '+' | '.join(map(str,bs))+' => '+expr
                       for expr,bs in groups.items())
        funcs.append(f'def potential{a} (b c : Nat) : Nat :=\n  match b with\n{body}\n  | _ => 0\n')
    model=HEADER+'\n'.join(funcs)+FOOTER+'end P196.Agent4.Saturation\n'
    cert='import PrefixModel\n\nnamespace P196.Agent4.Saturation\nset_option maxRecDepth 100000\nset_option maxHeartbeats 50000000\n'
    for a in range(1,19):
        cert+=f'theorem row{a} : ∀ b c : Fin 19, ∀ e : Fin 2, Check {a} b.val c.val e.val := by decide +kernel\n#print axioms row{a}\n\n'
    cert+='end P196.Agent4.Saturation\n'
    folder.mkdir(parents=True,exist_ok=True)
    (folder/'PrefixModel.lean').write_text(model)
    (folder/'SaturationCertificate.lean').write_text(cert)
    summary={'vertices':len(vertices),'edges':len(edges),'scale':K,
             'max_potential':max(potential),'max_rank':max(rank),
             'zero_slack_edges_including_controls':tight_count,
             'critical_cycle':CRITICAL,'edge_stream_sha256':edge_digest.hexdigest(),
             'prefix_model_sha256':sha256(model.encode()).hexdigest(),
             'certificate_sha256':sha256(cert.encode()).hexdigest(),
             'scope':'Exact finite edge certificate. All-period conclusions require the checked path theorem and its stated projection hypotheses.'}
    (folder/'saturation-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
    return summary

HEADER = 'import Lean.Elab.Tactic.Omega\n\n/-! Agent #4: exact three-column saturation obstruction.\nThe finite relation permits both incoming inner carries. It is a necessary\nprojection, not a claim that every abstract path has an ordinary integer lift.\n-/\nnamespace P196.Agent4.Saturation\n\nstructure Prefix where\n  a : Nat\n  b : Nat\n  c : Nat\n  deriving DecidableEq, Repr\n\ndef advance (s : Prefix) (e : Nat) : Prefix × Nat :=\n  let l1 := s.a / 10\n  let l2 := (s.b + l1) / 10\n  let d0 := s.a % 10\n  let d1 := (s.b + l1) % 10\n  let d2 := (s.c + l2) % 10\n  let r2 := (s.c + e) / 10\n  let r1 := (s.b + r2) / 10\n  let gamma := (s.a + r1) / 10\n  let h0 := (s.a + r1) % 10\n  let h1 := (s.b + r2) % 10\n  let h2 := (s.c + e) % 10\n  if gamma = 0 then (⟨d0+h0, d1+h1, d2+h2⟩, gamma)\n  else (⟨d0+1, d1+h0, d2+h1⟩, gamma)\n\n'

FOOTER = '\ndef potential (s : Prefix) : Nat :=\n  match s.a with\n  | 1 => potential1 s.b s.c\n  | 2 => potential2 s.b s.c\n  | 3 => potential3 s.b s.c\n  | 4 => potential4 s.b s.c\n  | 5 => potential5 s.b s.c\n  | 6 => potential6 s.b s.c\n  | 7 => potential7 s.b s.c\n  | 8 => potential8 s.b s.c\n  | 9 => potential9 s.b s.c\n  | 10 => potential10 s.b s.c\n  | 11 => potential11 s.b s.c\n  | 12 => potential12 s.b s.c\n  | 13 => potential13 s.b s.c\n  | 14 => potential14 s.b s.c\n  | 15 => potential15 s.b s.c\n  | 16 => potential16 s.b s.c\n  | 17 => potential17 s.b s.c\n  | 18 => potential18 s.b s.c\n  | _ => 0\n\ndef clock (s : Prefix) : Nat :=\n  match s.a, s.b, s.c with\n  | 8, 12, 9 => 0\n  | 17, 5, 0 => 1\n  | 8, 13, 5 => 2\n  | 17, 6, 11 => 3\n  | 8, 14, 8 => 4\n  | 17, 8, 17 => 5\n  | 8, 16, 16 => 6\n  | 17, 13, 14 => 7\n  | _, _, _ => 0\n\ndef Check (a b c e : Nat) : Prop :=\n  let s : Prefix := ⟨a,b,c⟩\n  let out := advance s e\n  82*out.2 + potential out.1 ≤ 41 + potential s ∧\n    (82*out.2 + potential out.1 = 41 + potential s →\n      clock out.1 = (clock s + 1) % 8)\n\ninstance (a b c e : Nat) : Decidable (Check a b c e) := inferInstanceAs\n  (Decidable (82*(advance ⟨a,b,c⟩ e).2 + potential (advance ⟨a,b,c⟩ e).1 ≤\n      41 + potential ⟨a,b,c⟩ ∧\n    (82*(advance ⟨a,b,c⟩ e).2 + potential (advance ⟨a,b,c⟩ e).1 =\n      41 + potential ⟨a,b,c⟩ →\n      clock (advance ⟨a,b,c⟩ e).1 = (clock ⟨a,b,c⟩ + 1) % 8)))\n\nset_option maxRecDepth 100000\nset_option maxHeartbeats 50000000\n\n\n'

if __name__ == "__main__":
    generate(Path(__file__).resolve().parent)
