#!/usr/bin/env python3
"""Agent #109: emit ProjK<g>.lean (chunked kernel projection checks) and the
assembled BoundaryCertificateK.lean."""
import math
sizes={0:24,1:76,2:324,3:910,4:2522,5:3434,6:3434,7:3434}
nxt={0:1,1:2,2:3,3:4,4:5,5:6,6:7,7:5}
M=400; MB=1000
hdr=lambda imp:[f"import {imp}","","namespace BoundaryCertificateK","open Sofic Sofic.Fast BoundaryCertificate","",
                "set_option maxRecDepth 100000","set_option maxHeartbeats 0",""]
def dispatch(K,name):
    if K==1: return f"  intro i hi\n  have : i = 0 := by omega\n  subst this\n  exact {name}0"
    alts=" ∨ ".join(f"i = {k}" for k in range(K))
    lines=[f"  intro i hi",f"  rcases (by omega : {alts}) with "+" | ".join("h" for _ in range(K))]
    for k in range(K): lines.append(f"  · subst h; exact {name}{k}")
    return "\n".join(lines)
for g in range(8):
    n=nxt[g]; K=math.ceil(sizes[g]/M); KB=math.ceil(sizes[g]/MB)
    out=hdr(f"FastData{g}")
    out.append(f"/-! Agent #109: kernel (`decide +kernel`) projection check for graph {g} → graph {n}, in chunks. -/\n")
    for k in range(K):
        out.append(f"theorem pairs{g}_{k} : pairsOK output graph{n}K T{g} B{g} H{g}\n    (((rawNodes fiber graph{g}K).drop ({k} * {M})).take {M}) = true := by decide +kernel\n")
    out.append(f"theorem pairs{g}_end : (rawNodes fiber graph{g}K).drop ({K} * {M}) = [] := by decide +kernel\n")
    for k in range(KB):
        out.append(f"theorem buckets{g}_{k} : bucketsOK B{g}\n    (((rawNodes fiber graph{g}K).drop ({k} * {MB})).take {MB}) = true := by decide +kernel\n")
    out.append(f"theorem buckets{g}_end : (rawNodes fiber graph{g}K).drop ({KB} * {MB}) = [] := by decide +kernel\n")
    out.append(f"theorem pairs{g}_all : pairsOK output graph{n}K T{g} B{g} H{g} (rawNodes fiber graph{g}K) = true := by\n  apply pairsOK_chunks _ _ _ _ _ {M} {K} _ _ pairs{g}_end\n"+dispatch(K,f"pairs{g}_")+"\n")
    out.append(f"theorem buckets{g}_all : bucketsOK B{g} (rawNodes fiber graph{g}K) = true := by\n  apply bucketsOK_chunks _ {MB} {KB} _ _ buckets{g}_end\n"+dispatch(KB,f"buckets{g}_")+"\n")
    out.append(f"theorem projection{g}_fast :\n    Projection fiber output graph{g}K graph{n}K (rankT T{g}) (projT T{g}) :=\n  fast_sound buckets{g}_all pairs{g}_all\n")
    out.append("end BoundaryCertificateK\n")
    out.append(f"#print axioms BoundaryCertificateK.projection{g}_fast")
    open(f"ProjK{g}.lean","w").write("\n".join(out)+"\n")
# assembled certificate
orsK=lambda k:"".join("Or.inr (" for _ in range(k))
out=["import ProjK0","import ProjK1","import ProjK2","import ProjK3","import ProjK4","import ProjK5","import ProjK6","import ProjK7","",
"/-! Agent #109: kernel-only replay of `BoundaryCertificate.lean` over the literal tables,",
"with the eight projection checks replaced by `Sofic.Fast` tree certificates. -/","",
"namespace BoundaryCertificateK","open Sofic Sofic.Fast BoundaryCertificate","",
"set_option maxRecDepth 100000","set_option maxHeartbeats 0","",
"theorem fibers_arithmetic_checked :","    ((List.range 88).all fun l =>","      (fiber l).all (fun i => i < 164) &&",
"      (List.range 164).all (fun i =>","        (fiber l).contains i == permitted l opts[i]!)) = true := by","  decide +kernel",""]
for g in range(8): out.append(f"theorem root{g}_checked : checkRoot graph{g}K 41 rootRanks{g}K = true := by decide +kernel")
out+=["","def Invariant (n : Nat) (w : Word) : Prop :=",
"  Accepts graph0K n w ∨ Accepts graph1K n w ∨ Accepts graph2K n w ∨",
"  Accepts graph3K n w ∨ Accepts graph4K n w ∨ Accepts graph5K n w ∨",
"  Accepts graph6K n w ∨ Accepts graph7K n w","",
"theorem invariant_preclosed {n : Nat} {old new : Word}",
"    (hnew : Invariant n new) (hcol : Column fiber output n old new) :",
"    Invariant n old := by",
"  rcases hnew with h | h | h | h | h | h | h | h"]
def inj(pos):  # position pos in 8-way disjunction
    s=orsK(pos)+("Or.inl (" if pos<7 else "")
    close=")"*(pos+(1 if pos<7 else 0))
    return s,close
for g in range(8):
    n=nxt[g]; s,c=inj(n)
    out.append(f"  · exact {s}projection_sound projection{g}_fast h hcol{c}")
out+=["","theorem root_excluded (n : Nat) : ¬ Invariant n (fun _ => 41) := by","  intro h","  rcases h with h | h | h | h | h | h | h | h"]
for g in range(8): out.append(f"  · exact checkRoot_sound root{g}_checked n h")
out+=["","/-- Kernel-only replay of `BoundaryCertificate.no_finite_exterior` (for the literal",
"transcription `graph0K` of `graph0`). -/",
"theorem no_finite_exterior {n : Nat} {target : Word}","    (ht : Accepts graph0K n target) :",
"    ¬ ReverseClosure.Path (Column fiber output n) (fun _ => 41) target := by",
"  apply ReverseClosure.excludes_reachable (root_excluded n) (Or.inl ht)",
"  intro p s hs hcol","  have hp := invariant_preclosed hs hcol","  refine ⟨?_, Or.inl hp⟩","  intro heq","  subst p","  exact root_excluded n hp","",
"end BoundaryCertificateK","",
"#print axioms BoundaryCertificateK.fibers_arithmetic_checked",
"#print axioms BoundaryCertificateK.invariant_preclosed",
"#print axioms BoundaryCertificateK.no_finite_exterior"]
open("BoundaryCertificateK.lean","w").write("\n".join(out)+"\n")
