# T7: exact global center equations 和 checked rational contradictions

## Result 和 scope

**PAPER PROOF + COMPUTED.** A frozen symmetric neutral-band center itinerary
compiles to exact integer linear equalities 和 inequalities. One symbolic
initial center generates every subsequent phase, so every temporal seam 和
the final return are joined. Rational elimination emits explicit row
multipliers; a separately authored checker verifies the resulting contradiction
without importing the compiler or trusting its reported status.

All eight main source certificates, Agent116's base20 certificate, 和 Agent101's
new decimal center pass their actual coefficient/carry/closure constraints.
Every one of the nine frozen nondecimal controls gives a checked rational
equality contradiction at base10. These exclude only the supplied frozen
itineraries. They do not exclude other decimal centers or full certificates.

The decimal positive is especially useful: its 24-step center closes, but its
full exterior B remains missing. This tool neither searches for B nor proves
that a supplied center driver is realizable by B. No new Lean theorem or
generic decimal impossibility is claimed.

## Exact input language

`center_itinerary.py` accepts `p196-center-itinerary-v1` with symmetry `required`
和 a nonempty list of phases. Phase t specifies:

- positive center width m_t;
- all m_t+1 binary normalization carries k_(t,0),...,k_(t,m_t);
- binary overflow g_t 和 nonnegative neutral-pair trim v_t.

The entering carry is e_t=k_(t,0), 和 the last carry must be 1-e_t.
Widths satisfy m_(t+1)=m_t+g_t-2v_t cyclically. Empty centers are excluded:
their unchanged entering/exiting carry cannot satisfy the required flip.
Trims may be nonmaximal. All arrays are least significant first.

The compiler uses ceil(m_0/2) independent initial symmetric coefficients 和
one symbolic base b. The requested target base is imposed by its own equality.
After that, every phase center is an affine expression in those same variables;
the compiler does not introduce independent copies at different phases.

For each source coefficient C_j it forms

    d_j = C_j + k_j - b*k_(j+1).

It records 0<=C_j<=2b-2 和 0<=d_j<=b-1. If g=1, it appends e*(b-1)
to the digit word. The raw next center is this word plus its reversal.
Every coefficient removed at either end must equal b-1. The remaining word
becomes the next symbolic center. Every final coefficient must equal its
original coefficient, including both sides of each symmetric pair.

Rows use `dot(coefficients, variables)=rhs`; inequality rows use `<=rhs`.
Labels identify coefficient/digit bounds, each left/right trim, closure,
和 target base. `origin.frozen_prefix_length` conservatively records how many
preceding phase assumptions a row can depend on. A row labelled phase t may
depend on earlier carries through propagated coefficients. Nonzero multiplier
labels are not a minimal set of carry assumptions.

## Why compilation is exact — PAPER PROOF

For an integer assignment with b>=2 satisfying all rows, digit bounds give

    C_j + k_j = d_j + b*k_(j+1),  0<=d_j<b.

Uniqueness of quotient 和 remainder, inductively from the supplied entering
carry, makes each k_j the actual normalization carry. The coefficient bounds
are exactly the A120 center bounds. The frozen last carry gives the flip.

The appended overflow digit 和 reverse sum are exactly A120 `nextC` for the
supplied e/g. Both trim boundaries are imposed literally, so the remaining
word is the actual next center. Propagation joins each edge to its successor;
the closing equalities join the last edge to the first. Initial symmetry is
built into the variable parameterization, 和 every reverse sum preserves it.

Conversely, a closed symmetric center trajectory with those exact carries,
widths, overflows, 和 trims supplies an integer assignment satisfying every
recorded row. This establishes equivalence for centers with the supplied
driver. It makes no assertion that any exterior realizes that driver.

## Independently checked contradiction semantics

The compiler performs exact Fraction elimination on equalities only, tracking
their original row combinations. A certificate supplies one rational weight
lambda_i per equality. `row_contradiction_check.py`, separately authored by
the Manager, checks:

    sum_i lambda_i*A_i = 0,    sum_i lambda_i*rhs_i != 0.

An assignment satisfying all equalities would make the same combination equal
on both sides, a contradiction. Therefore accepted certificates exclude even
rational solutions of those equalities, hence also bounded integer centers.

The independent checker validates inequality row syntax but does not use them.
Its acceptance certifies the supplied rows. The itinerary-to-row bridge is the
paper argument above, source review, 和 separate scalar-oracle controls below.

`NO_RATIONAL_EQUALITY_CONTRADICTION` is deliberately weaker than feasibility.
For example, one phase with width1, carries `[0,1]`, g=0, v=0 has equality
solution C=2b. At b=10 it gives C=20, violating the coefficient bound18.
The program reports no equality contradiction; it does not report SAT.
Integer divisibility certificates 和 inequality-based contradictions are not
implemented in this first certificate format.

## Concrete base26 certificate

The actual A120 base26 fixture is read from the existing registered
`Agent213KnownBaseMechanisms/KnownBases.lean`. Its initial center is
`[32,20,20,32]`. Independent compilation gives the following sufficient rows
for frozen-base10 inconsistency, with variables x0,x1,b:

| Row | Equality | Multiplier |
|---|---|---:|
| phase3 left trim | 4*x0-5*b=-2 | -61/16 |
| closure0 | 7*x0+4*x1-12*b=-8 | 11/4 |
| closure1 | 4*x0+11*x1-14*b=-16 | -1 |
| target base | b=10 | -1/16 |

Their weighted sum is exactly 0=1. At base26 the actual center satisfies every
equality 和 inequality. This calculation is derived directly from the A120
fixture; REPORT213 retains authorship of the earlier related center rigidity.

Agent116's base20 fixture similarly gives 14 variables,29 equalities,840
inequalities. Its phase6 trim row includes `64*x0-93*b=-68`; the full closure
system supplies the rational contradiction at b=10. The emitted proof retains
all weights explicitly:15 of29 equalities occur with nonzero weight. The
target-base row has weight -1/10; the remaining weighted rows give b/10=2.
Thus their sum with b=10 is exactly0=1. No minimal-support claim is made.

## Decimal center control 和 attribution

Agent101's [PR381](https://github.com/taco-jpg/p196-algorithm/pull/381), at
`f29759a359d923c7d8c1a22d7e7aecde462d565a`, supplies the center driver:

    e = 010100110100101011001011
    g = 110001001000110001001000
    v = 100001000000100001000000
    C0 = [9,14,13,18,13,14,9]

We independently reconstructed all24 centers by whole-integer normalization.
Every literal trim 和 temporal seam passes; the final C is C0. Its base10
system has5 variables,16 equalities,640 inequalities, all satisfied by its
actual initial half-center 和 base10. This is a credited center-only positive,
not a new discovery or full `cycleOK 10` certificate. Agent117/Agent101 retain
their full-B search scopes; no such search was run for this task.

Agent116's [PR356](https://github.com/taco-jpg/p196-algorithm/pull/356), at
`b7a718b78d67cf54d362232ba1b8f90fbec23af8`, supplies the base20 fixture.
Its complete independent arithmetic/Lean review preceded this tool. The nine
nondecimal controls 和 the new decimal fixture retain their original authors.
This contribution is the general row compiler, checked contradiction format,
separate validation, 和 reproducible combined controls.

## Reproduction 和 actual controls

From repository root:

```bash
python3 calculation/manager/test_center_itinerary.py
python3 calculation/manager/test_row_contradiction_check.py
python3 -O calculation/manager/test_row_contradiction_check.py
python3 calculation/manager/center_itinerary.py calculation/manager/base20_center_fixture.json --base 10 --system /tmp/center20-system.json --proof /tmp/center20-proof.json
python3 calculation/manager/row_contradiction_check.py /tmp/center20-system.json /tmp/center20-proof.json
python3 tools/verify.py --changed
```

Executed arithmetic controls:

- Ten positive bases/fixtures:2,4,8,16,32,26,11,17,20,10;88 actual center edges.
- Nine frozen nondecimal-to-decimal contradictions independently checked.
- 74,621 complete matrix entries compared against a separate scalar trajectory
  oracle, including50 synthetic carry/width itineraries. Affine basis
  evaluation compares every coefficient 和 constant, not just solution samples.
- 25 malformed API cases;10 normal/optimized CLI cases, including explicit
  resource exhaustion 和 stale-proof invalidation after early parsing errors.
- Nine independently authored adversarial checker test groups pass normally
  和 with Python `-O`; proof flags never use removable assertions.
- The entire compiler control summary is identical normally 和 with `-O`.

## Resource 和 artifact boundaries

Input limits are128 phases,510 coefficients per phase,4096 total phase widths,
256 variables,20000 rows per kind,4096-bit row integers, 和64MiB JSON input.
Elimination defaults to5,000,000 charged rational operations 和12000-bit
fractions. The independent checker accepts up to16384-bit proof integers,
with its own weighted-sum operation/accumulator guards. Limit exits are
UNDECIDED, never mathematical contradictions.

JSON readers reject duplicate keys, nonfinite constants, bools masquerading
as integers, 和 malformed dimensions. Compiler proof output is invalidated
before parsing so early failures cannot leave a stale accepted proof.
The supplied fixture files are mathematical data; generated systems/proofs
can be written outside the repository. No external service or solver is used.

The current tool does not minimize carry changes, enumerate alternative
itineraries, lift B, or decide arbitrary center widths/repetitions. It supplies
global seam evidence 和 a checkable reason that a particular frozen branch
must change. A rational equality certificate is not a new Lean endpoint.
