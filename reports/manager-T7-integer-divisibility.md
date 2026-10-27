# T7: independently checked integer row-divisibility obstructions

## Result 和 scope

**PAPER PROOF + COMPUTED.** The existing frozen-center compiler now has a
separate integer-certificate producer. It combines its supplied equality
rows with explicit integer multipliers 和 emits a row whose coefficient gcd
does not divide its right side. A separately authored checker recomputes
that row 和 gcd without importing the producer or itinerary compiler.

The base20 frozen itinerary at base10 already forces `64*x0=862` from just
one boundary row 和 the base row. Those two rows have a rational solution,
but no integer solution. A base26 three-row subsystem similarly forces
`11*x1=76`. These are additional short arithmetic obstructions, not new
global decimal exclusions. All ten genuine center fixtures remain positive,
including the 24-phase decimal center from Agent101. No B search is performed.

This extension is stacked on [PR395](https://github.com/taco-jpg/p196-algorithm/pull/395),
commit `97901a64c762b1bc506c8a1ad5e6b0624a18c45c`. Its seven source/report/data
files remain unchanged. There is no new Lean theorem, accepted decimal cycle,
complete integer-feasibility procedure, or claim that every frozen itinerary
with no emitted contradiction is feasible.

## Certificate 和 proof — PAPER PROOF

For original equality rows `A_i*x=r_i`, choose integer weights `w_i` 和 form

    c = sum_i w_i*A_i,     d = sum_i w_i*r_i,
    h = gcd(c_0,...,c_(n-1)).

Every integer solution would satisfy `c*x=d`. Since h divides every c_j,
it would divide their integer linear combination d. Thus `h>=2` 和 `h∤d`
certify that the supplied equalities have no integer solution.

The JSON proof format is `p196-integer-row-divisibility-v1`. It contains:

- `multipliers`: exactly one signed integer per supplied equality;
- `combined_coefficients`: the claimed n-dimensional integer vector c;
- `combined_rhs`: the claimed integer d;
- `coefficient_gcd`: the claimed nonnegative h.

`integer_divisibility_check.py` independently validates the system/proof
dimensions 和 strict integer types, recomputes c,d,h, requires exact matches
to all three claims, 和 checks `h>=2` and `d % h != 0`. Every variable enters
the gcd, including the base if its coefficient has not been canceled. A zero
coefficient row is outside this format; the existing rational checker handles
`0=d` contradictions. A gcd of one supplies no divisibility obstruction.

The checker imports only the existing independently authored row validator.
It validates inequality syntax but does not use inequalities. Neither
reported statuses nor origin labels are trusted as arithmetic evidence.
Acceptance proves inconsistency of the supplied integer equalities. Matching
those rows to an actual frozen center remains the separate compiler bridge
proved on paper 和 checked in
[the preceding report](manager-T7-carry-conflicts.md).

## Base20: a prefix obstruction before cycle closure

The initial center of Agent116's
[PR356](https://github.com/taco-jpg/p196-algorithm/pull/356) has width26.
Use its frozen carries, overflow/trim schedule, 和 symmetric initial variables
`x0,...,x12,b`. The compiler emits 29 equalities at target base10. In the
published phase convention:

| Original row index | Label | Equality | Integer weight |
|---:|---|---|---:|
| 0 | `p6.trim.left.0` | `64*x0-93*b=-68` | 1 |
| 28 | `target_base` | `b=10` | 93 |

All omitted weights are zero. The combination is `64*x0=862`, whose
coefficient gcd is64 和 remainder is30. The selected two-row subsystem is
rationally consistent: `b=10,x0=431/32`, with the unused initial variables
free. The existing rational-elimination tool correctly finds no equality
contradiction for that subsystem. The integer checker accepts its new proof.

At the actual base20, the same boundary row gives `64*x0=1792` 和 `x0=28`.
More generally this frozen prefix requires `93*b-68` divisible by64, hence
`b=20 mod64` (29 has inverse53 modulo64). This is a necessary congruence,
not sufficiency for the full center or a classification of possible bases.

The boundary row depends on the propagated phases0 through6, as its existing
`frozen_prefix_length=7` records. No closure row participates. Consequently,
changing only the later closing edge cannot repair this exact frozen prefix
at base10. A transfer must change an earlier carry, overflow/trim assumption,
or the initial width/symmetry parameterization. The two-row support is not a
minimal list of carries to change: a single propagated row contains a whole
prefix of assumptions.

## Base26: a distinct short subsystem

The existing A120 fixture from `Agent213KnownBaseMechanisms/KnownBases.lean`
starts with `[32,20,20,32]`; x0,x1 are its independent initial coefficients.
At target base10 the following three of seven rows suffice:

| Original row index | Label | Equality | Integer weight |
|---:|---|---|---:|
| 0 | `p3.trim.left.0` | `4*x0-5*b=-2` | -1 |
| 3 | `closure.1` | `4*x0+11*x1-14*b=-16` | 1 |
| 6 | `target_base` | `b=10` | 9 |

The combination is `11*x1=76`, with gcd11 和 remainder10. The three rows
have rational solution `(x0,x1,b)=(12,76/11,10)`, so this subsystem also
needs integer arithmetic to exclude it. At base26 the same difference gives
`11*x1=9*26-14=220`, satisfied by x1=20. The resulting necessary congruence
is `b=4 mod11`. This does not replace the full frozen-center rigidity already
credited to Agent213 和 reviewed in the preceding report.

## Producer method 和 honest nonconclusions

`integer_divisibility.py` accepts the unchanged `p196-center-affine-v1`
system format. It starts with original rows, using an explicit unit row
`b=target_base` first when one is present. This is an ordering heuristic;
its literal coefficients/right side, not a label, identify that equation.

For pivot coefficient p 和 current coefficient a, it lets g=gcd(p,a) 和
replaces the current row by `(p/g)*current-(a/g)*pivot`, applying the same
integer operation to the original-row weights. It checks the coefficient
gcd after every intermediate row. It never divides a row by its coefficient
gcd without retaining integer original-row weights. The first contradiction
is returned; no minimal-support or complete search claim is made.

The search is deliberately incomplete. For `2*x+y=0, y=1`, forward
elimination finds no divisibility certificate. Nevertheless weights `[1,-1]`
give `2*x=-1`, which the independent checker accepts. This explicit regression
prevents `NO_DIVISIBILITY_CERTIFICATE_FOUND` from being mistaken for integer
feasibility. A separate center regression has an integer equality solution
`C=20,b=10` which violates `C<=18`; equality arithmetic does not decide the
inequalities either. Resource exits are `RESOURCE_LIMIT_UNDECIDED`.

## Reproduction 和 executed controls

From repository root:

```bash
python3 calculation/manager/test_integer_divisibility.py
python3 calculation/manager/test_integer_divisibility_check.py
python3 -O calculation/manager/test_integer_divisibility_check.py
python3 calculation/manager/center_itinerary.py calculation/manager/base20_center_fixture.json --base 10 --system /tmp/center20-system.json
python3 calculation/manager/integer_divisibility.py /tmp/center20-system.json --proof /tmp/center20-integer-proof.json
python3 calculation/manager/integer_divisibility_check.py /tmp/center20-system.json /tmp/center20-integer-proof.json
python3 tools/verify.py --changed
```

The new producer suite passes identically in ordinary 和 optimized Python:

- Ten actual center controls: bases2,4,8,16,32,26,11,17,20,10;88 edges.
- Nine frozen nondecimal itineraries at base10 yield independently verified
  integer-divisibility certificates. They retain the original authorship of
  the fixtures 和 do not exclude different decimal itineraries.
- Both short subsystems above have independently evaluated explicit rational
  solutions 和 independently checked integer obstructions.
- Sixty generated signed systems with known integer solutions yield no
  false contradiction; three explicit nonconclusion controls pass.
- Fifteen malformed API cases, operation/bit limits, 和16 CLI controls cover
  normal/optimized execution, duplicate keys, nonfinite values, deeply nested
  input, stale-proof invalidation, 和 same-file/hardlink output aliases.
- Eight independently authored checker groups pass normally 和 with `-O`,
  including signed weights, every-variable gcd, altered row/RHS/gcd/weights,
  gcd0/1 rejection, malformed integers, 和 resource guards.

## Resource limits 和 provenance boundaries

The producer uses the preceding validator's limits:256 variables,20000 rows
per kind,4096-bit row integers,64MiB input. It charges at most5,000,000 scalar
row/weight updates 和 coefficient-gcd visits, including base-row inspection.
Intermediate rows 和 weights are limited to12000 bits. The independent
checker accepts16384-bit proof integers 和 retains separate2,000,000-addition
和1,048,576-bit accumulator limits. A user's operation setting may lower,
but not raise, the producer's cap. None of these limits is a completeness
bound for integer feasibility.

After CLI arguments 和 distinct paths are validated, proof files are replaced
with an explicit nonproof marker before reading the system JSON. Input-reading
or computation failures, absence of a certificate, 和 resource exits cannot
silently reuse an earlier accepted proof. Aliases are rejected before writing.
The producer uses exact integers, 和 its checker independently repeats all
certificate arithmetic. No numerical optimization or external solver is used.

The decimal positive is Agent101's center from
[PR381](https://github.com/taco-jpg/p196-algorithm/pull/381), not a full
decimal `cycleOK` witness. This extension neither revisits its B-lift searches
nor establishes a generic obstruction to decimal Lychrel certificates.
