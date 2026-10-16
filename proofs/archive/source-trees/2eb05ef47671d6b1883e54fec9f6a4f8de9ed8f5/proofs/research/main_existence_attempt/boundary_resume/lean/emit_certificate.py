"""Transcribe independently checked rank arrays; Lean replays every obligation.

The text parser and each finite check are ordinary Lean definitions. No proof
is imported from Python and no generated declaration is an axiom.
"""
from pathlib import Path
import json, hashlib

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent/'reverse'
cert=json.loads((SOURCE/'sofic_rank_certificate.json').read_text())
local=json.loads((SOURCE/'local_inverse_tables.json').read_text())

def nums(values): return ' '.join(map(str,values))
def arr(values): return 'parseNats "'+nums(values)+'" |>.toArray'
def edge_code(e):
    u,v,l=e
    assert 0<=u<4096 and 0<=v<4096 and 0<=l<4096
    return (u*4096+v)*4096+l

out=['''import SoficProof

/-!
Literal finite rank/projection data for the eight cyclic-language graphs.
The source JSON is not trusted: BoundaryCertificate.lean checks every raw
preimage edge against ordinary decimal arithmetic and proves exclusion.
Data-source SHA256: '''+hashlib.sha256((SOURCE/'sofic_rank_certificate.json').read_bytes()).hexdigest()+'''
-/

namespace BoundaryCertificate
open Sofic

def parseNats (s : String) : List Nat := (s.splitOn " ").filterMap String.toNat?
def decodeEdge (n : Nat) : LEdge :=
  {src := n / 16777216, dst := n / 4096 % 4096, lab := n % 4096}
def parseGraph (s : String) : Graph := (parseNats s).map decodeEdge

structure Opt where
  q : Nat
  a : Nat
  b : Nat
  c : Nat
  e : Nat
  r : Nat
  deriving DecidableEq, Repr, Inhabited

instance : BEq Opt := ⟨fun a b => decide (a = b)⟩
instance : LawfulBEq Opt where
  eq_of_beq := of_decide_eq_true
  rfl := by intro a; exact decide_eq_true rfl

def opts : Array Opt := #[
''']
options=local['options']
out.append(',\n'.join('  ⟨'+', '.join(map(str,o))+'⟩'for o in options))
out.append('\n]\n')
out.append('def fibers : Array (List Nat) := #[\n')
out.append(',\n'.join('  ['+', '.join(map(str,f))+']'for f in local['fibers']))
out.append('\n]\n\ndef fiber (l : Nat) : List Nat := fibers[l]!\n')
out.append('''
/-- Adjacent local inverse options emit the preceding temporal letter. -/
def output (i j : Nat) : Option Nat :=
  let x := opts[i]!
  let y := opts[j]!
  let lo := (x.r + x.b) % 10 + x.e
  let hi := y.q + 1
  if lo ≤ hi && hi ≤ lo + 10 then
    let z := hi - lo
    if (z != 0 || x.e == 1) && (z != 10 || x.e == 0) then
      some (((x.a * 2 + x.b) * 2 + x.c) * 11 + z)
    else none
  else none

/-- Direct decimal inverse-fiber equations, using z+1 to avoid signed encoding. -/
def permitted (l : Nat) (x : Opt) : Bool :=
  l < 88 && x.q ≤ 18 && x.a ≤ 1 && x.b ≤ 1 && x.c ≤ 1 && x.e ≤ 1 && x.r ≤ 18 &&
  x.r + 1 == l % 11 + 10 * x.e &&
  (!(x.r < 9) || x.e == 0) && (!(x.r > 9) || x.e == 1) &&
  (x.q + x.a) / 10 == l / 44 &&
  (x.q + x.a) % 10 + (x.q + (l / 11 % 2)) % 10 == x.r &&
  (x.r + x.b) / 10 == l / 22 % 2 &&
  x.c == (x.q + (l / 11 % 2)) / 10

''')
for k,g in enumerate(cert['graphs']):
    out.append(f'def graph{k} : Graph := parseGraph "'+nums(map(edge_code,g['edges']))+'"\n')
for k,t in enumerate(cert['transitions']):
    out.append(f'def ranks{k} : Array Nat := '+arr(t['rank'])+'\n')
    out.append(f'def maps{k} : Array Nat := '+arr(max(0,m)for m in t['mapping'])+'\n')
for k,r in enumerate(cert['root_ranks']):
    out.append(f'def rootRanks{k} : Array Nat := '+arr(r)+'\n')
out.append('\nend BoundaryCertificate\n')
(HERE/'BoundaryData.lean').write_text(''.join(out))
print('BoundaryData.lean:',(HERE/'BoundaryData.lean').stat().st_size,'bytes')
