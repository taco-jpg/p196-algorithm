# Exact semantic refinement and inverse-family obstruction

**No nonempty safe forward-closed language, decimal Lychrel witness, or
proof for 196 was found.** This pass establishes three structural results
with explicit scope, rather than increasing observation depth again.

1. Adaptive finite-memory acceptance over the same complete configuration
   classes cannot evade a terminating representative. Universal safety and
   universal transition coverage project to an ordinary safe closed union
   of those classes. The previous 146 class exclusions therefore survive
   arbitrary mode switching of this kind.
2. The regular candidate `F10 = S2 intersect first-eleven-output safety`
   cannot be made forward closed by **any finite symmetric difference**.
   An explicit infinite family supplies a fresh closure failure beyond
   every finite set of added or deleted words.
3. No image has folded prefix `(1,6,2)`, and no two-step image has folded
   prefix `(2,12,4)`. This blocks every extension above the selected inverse
   family, at every width. It does not block all inverse branches above the
   original gate family.

The exact quantifiers, carry proof, certificate interface and limitations
are in `METHOD_AND_PROOF.md`.

## Infinite closure counterexamples

Write `q^s` for a run of s copies of the pair sum q. For every integer r>=5,
define canonical folded words as follows; only Q has a center.

| Family | Outer-to-inner pair prefix | Center | First positive palindrome time |
|---|---|---|---:|
| A_r | `(2,12,4,4,9^(r-5),14,16,16,15)` | absent | 14 |
| B_r | `(5,4,9^(r-2),14,14,12)` | absent | 13 |
| C_r | `(10,9^r,10,6)` | absent | 12 |
| Q_r | `(1,1,0^(r-1),1,7)` | 12 | 11 |

The exact folded reverse-add map satisfies

`A_r -> B_r -> C_r -> Q_r`.

The final first-hit-eleven theorem is independently replayed from
`../tails/symbolic_tail_certificates.json`. All A and B words are safe,
so C_r belongs to S2. C_r is in F10 while its image Q_r is outside F10.
Their widths are 2r+6 and 2r+7. A finite edit set has a largest width,
so choosing a sufficiently large r preserves this closure failure.
This proves the finite-excision obstruction for the entire infinite family,
not just for sampled parameter values.

`check_inverse_ladder.py` checks three affine polynomial transitions and
replays all eleven transitions of the tail proof. It also checks 32
ordinary-integer cases, including r=1024, totaling 400 additions. Root's
separate replay is retained in `root_inverse_ladder_replay.log`.

## Exact limit of the selected inverse construction

For every r>=6 there is one further explicit ancestor,

`D_r = (1,6,2,2,4,9^(r-6),17,7,18,7)`, with no center,

and `G(D_r)=A_r`. Its first positive palindrome time is 15. The all-width
prefix obstruction proves that D_r has no predecessor, and that **every**
predecessor of any A_r is predecessorless. Thus A_r has exact maximum
backward depth one for r>=6. A_5 has no predecessor, as separately checked
by complete finite inverse enumeration. This construction cannot supply
unbounded delay by repeatedly extending this selected branch.

`prefix_obstruction_certificate.json` lists the complete local frontiers.
`check_prefix_obstruction.py` independently checks 76 ordinary next-pair
edges and 20 odd-center cases. It separately controls all 99,999 positive
integers below 100,000 and all 71,478 canonical six-/seven-digit pair words,
including the short odd-center transition. The symbolic D-to-A identity
holds for all r>=7, with r=6 handled directly; seven integer trajectories
control first hit 15.

The stronger full-column version is also proved in the separately owned
Lean module `../lean/prefix/PrefixObstruction.lean`. Its principal results
are `no_output_prefix_one_six_two`, `prefix_two_twelve_four_inverse`,
`no_two_step_prefix_two_twelve_four`, and `numeric_after_two_no_prefix`,
in namespace `DecimalPrefixObstruction`. The source and fresh-build audit
belong to that directory. No assumption of Lychrel existence is used.

## Other inverse branches really escape this cylinder

Complete safe inverse trees for r=5,...,8, through depth six, were preserved
and independently reconstructed from local decimal equations. Counts at
successive depths are:

| r | Depth 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 6 | 9 | 19 | 22 | 22 | 21 |
| 6 | 6 | 14 | 36 | 61 | 53 | 64 |
| 7 | 6 | 22 | 71 | 127 | 164 | 204 |
| 8 | 6 | 35 | 137 | 294 | 466 | 794 |

The audit checks 2,659 safe edges and 1,613 distinct inverse targets,
including the additional selected-family probes. These are finite counts,
not an all-r growth law or a proof of unbounded safe ancestry.

For example, `994999060500005` has folded prefix `(14,9,4)`, reaches Q_5
after three additions, and first reaches a palindrome at addition 14.
`outside_A_cylinder_witness.json` records its full integer trajectory.
Consequently, the prefix theorem cannot be promoted to a bound on all
ancestors of Q_r. No general backward obstruction for those escaping
branches was proved.

## Preserved finite probes and remaining gap

All discovery code, configurations, results, failures and logs are retained.
The large exploratory record is compressed as `exploration_archive.json.gz`.
Its independent checker verifies:

- 72 extended gate cases at horizon 60: 41 first hits and 31 UNKNOWN;
- 2,508 single-symbol insertion catalog entries, including 24 noncanonical
  entries, with no candidate retaining the required class and first hit
  for every tested repetition from 4 through 12;
- the previous complete 342-entry unary-prefix loop catalog: three exact
  class matches, none terminating within its horizon 20, hence no pump
  certificate in that specified finite catalog;
- every saved inverse node and edge, full S2 subset where recorded, and
  every saved ordinary-integer orbit.

The insertion and unary-loop failures do not exclude more general pumps.
UNKNOWN gate cases remain UNKNOWN. The projection theorem excludes only
controllers saturated under the same fixed configuration equivalence;
genuinely finer semantic languages are not ruled out. The finite-excision
theorem excludes finite repairs of F10, not arbitrary infinite refinements.
The inverse-prefix theorem excludes the selected cylinder, not the entire
gate's ancestry. No acceptance model satisfying all obligations in
`closure_certificate_interface.json` has been instantiated.

## Reproduce

Run from this directory; checks use only the standard library and existing
saved certificate data.

```sh
python3 -B check_inverse_ladder.py
python3 -B check_prefix_obstruction.py
python3 -B check_exploration_archive.py
```

Discovery regeneration is optional:

```sh
python3 -B inverse_ladder_certificate.py
python3 -B prefix_obstruction_certificate.py
python3 -B exploration_archive.py
python3 -B pump_search.py --seconds 90 --max-prefix 60 --max-hit 20
```

The symbolic conclusions rely on the checked identities and universal carry
arguments, not on the integer controls. The archive's finite counts have
independent arithmetic and inverse-graph replay. No prior pass was modified
and this worker performed no remote publication.
