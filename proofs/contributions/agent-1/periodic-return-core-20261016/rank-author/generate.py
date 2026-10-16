#!/usr/bin/env python3
"""Emit local finite certificates from the preserved partition and exact graph."""
from pathlib import Path
from collections import defaultdict, Counter
import gzip
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
ARCHIVE = ROOT / 'proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/outer_filtered_graph.json.gz'
SOURCE = ROOT / 'proofs/Agent1PeriodicOuterRank.lean'
sha = lambda b: hashlib.sha256(b).hexdigest()
compressed = ARCHIVE.read_bytes()
decoded = gzip.decompress(compressed)
assert sha(compressed) == 'c3eb0a4bd4bc8e390d7681746e66300851035dff1b102412e2d14977ed1088e5'
assert sha(decoded) == 'cbd5c62ac2af58d0d0ce1cbb6f0cf9199ac49c75291d062179caf15f96e1ad50'
data = json.loads(decoded)
key = lambda s: (tuple(s[0]), s[1])
components = {key(s): c for c, nodes in enumerate(data['components']) for s in nodes}
assert len(components) == sum(map(len, data['components'])) == 878
phase_labels = defaultdict(dict)
for (w, q), c in components.items():
    phase_labels[w][q] = c
constant = {(0, 0, 0, 0): 131, (9, 9, 9, 9): 129, (18, 18, 18, 18): 130}
overrides = {w: {q: c for q, c in qs.items() if c != 8}
             for w, qs in phase_labels.items() if w not in constant}
overrides = {w: qs for w, qs in overrides.items() if qs}
assert sum(map(len, overrides.values())) == 128
lookup = lambda s: constant.get(s[0], overrides.get(s[0], {}).get(s[1], 8))
assert all(lookup(s) == c for s, c in components.items())
rank = lambda c: 132 - min(c, 131)
edge_counts = Counter()
for row in data['graph']:
    s = key(row['source']); c = lookup(s)
    for edge in row['edges']:
        t = key(edge['target']); d = lookup(t)
        assert rank(d) <= rank(c)
        if c != d:
            assert 1 + rank(d) <= rank(c)
            edge_counts['cross'] += 1
        else:
            assert c in [8, 129, 130, 131]
            edge_counts[str(c)] += 1
    assert c != 131 or s[0] == (0, 0, 0, 0)
    if s[0] == (14, 14, 4, 4) and c in [8, 129, 130]:
        assert s[1] in [9, 10]
catalog = (ROOT / 'proofs/Agent1PeriodicOuterCatalog.lean').read_text()
node_blocks = dict(re.findall(r'private def outerNodes(\d\d) : List OuterNode := (\[.*?\n\])', catalog, re.S))
edge_blocks = dict(re.findall(r'private def outerEdges(\d\d) : List OuterEdge := (\[.*?\n\])', catalog, re.S))
assert len(node_blocks) == len(edge_blocks) == 59
assert sum(v.count('  ([') for v in node_blocks.values()) == 878
assert sum(v.count('  ⟨') for v in edge_blocks.values()) == 1458
word = lambda w: '[' + ','.join(map(str, w)) + ']'
intro = '''import Agent1PeriodicOuterCatalog

/-!
Local rank and label facts for the exact original outer graph. Component labels
are the preserved partition indices; this file proves neither SCC maximality
nor reachability. Closed checks are split by the original 59 source phases.
-/

set_option maxRecDepth 16384
set_option maxHeartbeats 16000000

namespace Agent1.Periodic
open Agent8

/-- Original partition labels on catalog nodes, with a total default off catalog. -/
def outerComponent (s : OuterNode) : Nat :=
  match s.1 with
'''
for w, c in sorted(constant.items()):
    intro += f'  | {word(w)} => {c}\n'
for w, qs in sorted(overrides.items()):
    intro += f'  | {word(w)} => match s.2 with\n'
    for q, c in sorted(qs.items()):
        intro += f'    | {q} => {c}\n'
    intro += '    | _ => 8\n'
intro += '''  | _ => 8

/-- Reverse the stored indices; saturation makes the rank positive everywhere. -/
def componentRank (c : Nat) : Nat := 132 - min c 131

theorem componentRank_pos (c : Nat) : 0 < componentRank c := by
  have h := Nat.min_le_right c 131
  unfold componentRank
  omega

private def edgeRankCheck (e : OuterEdge) : Bool :=
  decide (componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source) ∧
    (outerComponent e.source ≠ outerComponent e.target →
      1 + componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source)) ∧
    (outerComponent e.source = outerComponent e.target →
      outerComponent e.source ∈ [8,129,130,131]))

private def nodeLabelCheck (s : OuterNode) : Bool :=
  decide ((outerComponent s = 131 → s.1 = [0,0,0,0]) ∧
    (s.1 = [14,14,4,4] → outerComponent s ∈ [8,129,130] → s.2 = 9 ∨ s.2 = 10))

/- Structural list assembly follows the existing private catalog checker;
   no graph-theoretic soundness principle is introduced here. -/
private inductive RankBlocksAll {α : Type} (f : α → Bool) : List (List α) → Prop
  | nil : RankBlocksAll f []
  | cons {n ns} (hn : n.all f = true) (hs : RankBlocksAll f ns) :
      RankBlocksAll f (n :: ns)

private theorem RankBlocksAll.flatten {α : Type} {f : α → Bool}
    {ns : List (List α)} (h : RankBlocksAll f ns) : ns.flatten.all f = true := by
  induction h with
  | nil => rfl
  | cons hn hs ih => simp only [List.flatten_cons, List.all_append, hn, ih, Bool.and_self]

'''
parts = []
for label in sorted(node_blocks):
    parts.append(f'private def rankNodes{label} : List OuterNode := {node_blocks[label]}\n\n'
                 f'private def rankEdges{label} : List OuterEdge := {edge_blocks[label]}\n\n'
                 f'private theorem nodeCheck{label} : rankNodes{label}.all nodeLabelCheck = true := by decide\n\n'
                 f'private theorem edgeCheck{label} : rankEdges{label}.all edgeRankCheck = true := by decide\n\n')
tail = ''
for kind, stem, predicate in [('Node', 'Nodes', 'nodeLabelCheck'), ('Edge', 'Edges', 'edgeRankCheck')]:
    tail += f'private def rank{kind}Blocks : List (List Outer{kind}) :=\n  [' + ', '.join('rank' + stem + i for i in sorted(node_blocks)) + ']\n\n'
    tail += f'private theorem rank{kind}Blocks_eq : rank{kind}Blocks.flatten = outer' + ('Catalog' if kind == 'Node' else 'Edges') + ' := by rfl\n\n'
    expression = 'RankBlocksAll.nil'
    for label in reversed(sorted(node_blocks)):
        expression = f'RankBlocksAll.cons {kind.lower()}Check{label} ({expression})'
    tail += f'private theorem rank{kind}Blocks_checked : RankBlocksAll {predicate} rank{kind}Blocks :=\n  {expression}\n\n'
    tail += f'private theorem all{kind}s_checked : outer' + ('Catalog' if kind == 'Node' else 'Edges') + f'.all {predicate} = true := by\n  rw [← rank{kind}Blocks_eq]\n  exact RankBlocksAll.flatten rank{kind}Blocks_checked\n\n'
tail += '''/-- Every listed edge weakly decreases the concrete component rank. -/
theorem outerEdge_rank_le (e : OuterEdge) (he : e ∈ outerEdges) :
    componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source) := by
  have h := of_decide_eq_true (List.all_eq_true.mp allEdges_checked e he)
  exact h.1

/-- A change of stored component label costs at least one unit of rank. -/
theorem outerEdge_rank_drop (e : OuterEdge) (he : e ∈ outerEdges)
    (hne : outerComponent e.source ≠ outerComponent e.target) :
    1 + componentRank (outerComponent e.target) ≤ componentRank (outerComponent e.source) := by
  have h := of_decide_eq_true (List.all_eq_true.mp allEdges_checked e he)
  exact h.2.1 hne

/-- A listed internal edge can only have one of these four original labels. -/
theorem outerEdge_internal_component (e : OuterEdge) (he : e ∈ outerEdges)
    (heq : outerComponent e.source = outerComponent e.target) :
    outerComponent e.source ∈ [8,129,130,131] := by
  have h := of_decide_eq_true (List.all_eq_true.mp allEdges_checked e he)
  exact h.2.2 heq

/-- The stored zero label has exactly the required zero-phase implication. -/
theorem outerComponent_zero_phase (s : OuterNode) (hs : s ∈ outerCatalog)
    (hc : outerComponent s = 131) : s.1 = [0,0,0,0] := by
  have h := of_decide_eq_true (List.all_eq_true.mp allNodes_checked s hs)
  exact h.1 hc

/-- Initial-phase nodes in the three surviving labels have outside nine or ten. -/
theorem outerComponent_initial_core (s : OuterNode) (hs : s ∈ outerCatalog)
    (hphase : s.1 = [14,14,4,4]) (hc : outerComponent s ∈ [8,129,130]) :
    s.2 = 9 ∨ s.2 = 10 := by
  have h := of_decide_eq_true (List.all_eq_true.mp allNodes_checked s hs)
  exact h.2 hphase hc

end Agent1.Periodic

#print axioms Agent1.Periodic.componentRank_pos
#print axioms Agent1.Periodic.outerEdge_rank_le
#print axioms Agent1.Periodic.outerEdge_rank_drop
#print axioms Agent1.Periodic.outerEdge_internal_component
#print axioms Agent1.Periodic.outerComponent_zero_phase
#print axioms Agent1.Periodic.outerComponent_initial_core
'''
source = intro + ''.join(parts) + tail
assert not SOURCE.exists(), 'Preserve prior source before regeneration'
SOURCE.write_text(source)
probe = HERE / 'probe-source'
probe.mkdir(exist_ok=False)
(probe / 'RankPhaseProbe.lean').write_text(intro + parts[0] + parts[4] + '\nend Agent1.Periodic\n')
receipt = {'classification': 'FINITE_DIAGNOSTIC_AND_SOURCE_GENERATION_NOT_A_PROOF',
           'compressed_sha256': sha(compressed), 'decoded_sha256': sha(decoded),
           'outer_catalog_sha256': sha(catalog.encode()), 'generated_source_sha256': sha(source.encode()),
           'component_count': len(data['components']), 'node_count': len(components),
           'phase_count': len(node_blocks), 'transient_override_count': 128,
           'stored_membership_matches_generated_function_on_all_nodes': True,
           'edge_counts': dict(edge_counts),
           'checks': 'Original stored labels; no graph search or SCC recomputation. Per-phase literals copied exactly from pinned OuterCatalog; Lean will certify flatten equality and each local property.'}
(HERE / 'generation.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt))
