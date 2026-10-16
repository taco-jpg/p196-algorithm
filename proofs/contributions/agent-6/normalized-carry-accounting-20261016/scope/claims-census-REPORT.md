# Source census: normalized coordinate carry versus original certificate carry

## Scope decision

The useful next interface is to identify the normalized row's `overflowBit`
with the original Agent109 checker carry `gam`, then replace the indicator sum
in `checked_row_weighted_balance` by Agent110's existing `totalGam`.
This closes an explicit interface gap in the published PR115 source.

The raw `gam` to rho-threshold wrapper alone has lower priority. Its arithmetic
is already supplied by the existing normalizer correspondence and Agent6's
threshold theorem, and Agent110 previously exported a raw-checker carry bridge
to the Agent2 normalizer. The normalized-carry/accounting interface is more
reusable: it would connect the new coordinate balance to the original finite
width and band-gain accounting, without replacing either source.

**This packet is read-only source design. No theorem claim, proof source,
Lean execution, or Git mutation was made as part of this census.** Proposed
statements are recorded as unproved in `UNPROVED_TARGETS.json`. The completed
complementary landscape scan found no equivalent native carry/trim or normalized
state-carry theorem within its exact inspected scope. Its report and receipts
are preserved in `export-scan/`. Subsequent ownership and proof work belong to
separate tasks.

## Exact source and ownership pins

All twelve legacy source captures were read directly at main commit
`f44c06c4851b26523bcec920d93a52b93fd2a0a6`. Every captured legacy file matches its
historical Git blob and its original path at the source-map base
`2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. The Agent6 coordinate and certificate
consumer sources were read at published PR115 checkpoint
`937c33ba3a98b9778bfee45a0bf2f0c0b3765055`.

The claim census is pinned at coordination
`5d54351a6cf3375351f2cf985e9ef40854a0dd8c`, observed 2026-10-16 21:57:10 UTC,
with 129 task files. Eleven relevant claim payloads were verified byte for byte
against that tree. A later read-only landscape census reported 132 tasks at
`32b2f562b54f5d14ce0d45ed2fd5368fa8cd8004` and main
`7b9e663b3c40aadfd7038f264729f6b7e3c7ce88`; its main delta adds Agent100 GroupII
source/evidence and an Agent11 ledger correction, rather than modifying these
carry sources. The parent still performs a fresh guarded ownership check.

| Source | Exact Git blob | Role |
| --- | --- | --- |
| `TemplateStep__8873883b39064515.lean` | `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d` | Original norm, constant-band carry, bounds, data |
| `ReturnCertificate__b037c18e81a43bb5.lean` | `95196cfe2da9b224412a9c31910163cf5784f996` | Original State, gam, check and soundness |
| `OuterBridge__04b27506596f5de1.lean` | `06ed5a8660e83b2dde192a10c822c9317a79483b` | Existing normalizer equality and suffix decomposition |
| `ExteriorNormalization__e03ef2b2c3a7fcaa.lean` | `899eeebdf7c771921303ebaa720fd8ed5454fd36` | Agent116 padding and partial-trim source |
| `CertificateExterior__94efd9fc73b36162.lean` | `76e86aea561288b8a47f1b5999c2578e50d597c4` | Original normalized state projection |
| `CertificateCharge__46feaa8077e59426.lean` | `8af8e26c4112b5074b6b9e8e39c77cc416054c86` | Existing Agent110 raw carry bridge |
| `ExteriorCharge__52cbb237030a07b3.lean` | `3020c27a4f65aa5c59a76d2facecc6739fc25d00` | Agent2 normalizer and carry definition |
| `ExteriorFactorizationProof__c2d8a9a4ee47c405.lean` | `9a9a0e3e8335b218d2863edaee58c2c26614c0ca` | Existing normalize-value and rho padding arithmetic |
| `CoordinateThreshold.lean` | `34ddc74962d8bbef954f1626a80593de60906215` | Unconditional high-value formula; bounded carry bit |
| `CoordinateCycle.lean` | `6b7ab7b9801109f3a5af7e8237f59db84601686a` | Normalized indicator and weighted observables |
| `CertificateCoordinates.lean` | `958b7b77401171f3c05258c4d93fa8d5e21562f4` | Published weighted row balance awaiting this bridge |
| `CertificateAccounting__ad0d1bd9b0242036.lean` | `79bf1fdfebabcf95dee96698be9aab3747c2599a` | Original totalGam and exact band-gain relation |

Full repository paths, source commits, original paths, imports, byte counts,
SHA256 values and read URLs are in `source-pins.json`. Byte-identical source
captures use `.source.txt` names in `source-captures/`; no new `.lean` file was
created. `INTERFACES.json` contains forty-eight literal existing declaration
statements with their exact source lines and blob pins.

## Existing normalization and carry interfaces

In namespace `Agent109`, the original definitions include:

```lean
def kOf (x : Nat) : Nat := if 10 ≤ x then 1 else 0
def tOf (x : Nat) : Nat := x - 9 * kOf x
def Bounded (w : Word) : Prop := ∀ x ∈ w, x ≤ 18
def Phase (x : Nat) : Prop := 1 ≤ x ∧ x ≤ 17 ∧ x ≠ 9
```

The `γ` field of `data c B A C` is definitionally
`(norm B.reverse (kOf c)).2`; neither `A` nor `C` enters that field.
In namespace `Agent109.Cert`:

```lean
def gam (s : State) : Nat := (data s.c s.B s.A s.C).γ
```

The existing normalizer correspondence is unconditional:

```lean
Agent109.Outer.normalize7_eq (w : Word) (e : Nat) :
  P196.Agent7.Finite.normalize w e = Agent109.norm w e
```

Agent6's `phaseCarry c` and Agent109's `kOf c` are the same conditional. Thus
raw `gam s = Agent6.ExteriorCoordinates.overflow s.c s.B` is a direct consumer
of this existing theorem for arbitrary states, without a phase or coefficient
premise. It would not establish a new normalizer correspondence.

An older exported bridge already exists:

```lean
Agent110.CertificateBudget.gam_eq_overflow (s : State) (hc : s.c ≤ 18) :
  gam s = Agent2Exterior.overflow s.c s.B
```

Here Agent2's carry uses incoming `c / 10`, so its source includes
`kOf_eq_div (c : Nat) (hc : c ≤ 18) : kOf c = c / 10` and
`norm_eq_normalize (w : Word) (e : Nat) : norm w e = Agent2Exterior.normalize w e`.
Those existing declarations must retain Agent110 attribution. Importing the
entire charge package is unnecessary for the proposed Agent7 consumer because
`normalize7_eq` already compares the exact two normalizers required here.

Two existing bounds/formulas have no phase premise:

```lean
Agent109.gamma_le (c : Nat) (B A C : Word) (hB : Bounded B) :
  (data c B A C).γ ≤ 1

Agent6.ExteriorCoordinates.overflow_eq_highValue (c : Nat) (B : List Nat) :
  overflow c B = (highValue B + phaseCarry c) / 10 ^ B.length
```

Consequently, unlike the rho quotient theorem, this indicator/carry comparison
does not inherently require `c ≤ 17` or `c ≠ 9`.

## Existing padding argument and the precise structural gap

The required fixed incoming carry through an arbitrary phase suffix is already
an exported Agent109 theorem:

```lean
Agent109.norm_band_tail (x m : Nat) (hx : x ≤ 18) :
  norm (List.replicate m x) (kOf x) =
    (List.replicate m (tOf x), kOf x)

Agent109.norm_append (a b : Word) (e : Nat) :
  norm (a ++ b) e =
    ((norm a e).1 ++ (norm b (norm a e).2).1,
     (norm b (norm a e).2).2)

Agent109.Outer.stripSuffix_spec (c : Nat) (w : Word) :
  ∃ j, w = stripSuffix c w ++ List.replicate j c
```

Agent116's existing `Br_append_phase` theorem has public premises `Phase c` and
`Bounded B` because its full result controls both sides of the returned word.
Its local `hright` has the more specific equality:

```lean
norm (B ++ [c]).reverse (kOf c) =
  ([tOf c] ++ (norm B.reverse (kOf c)).1,
   (norm B.reverse (kOf c)).2)
```

The source establishes `hright` using `norm_append` and
`norm_band_tail c 1 hc18`; the coefficient bound and `c ≠ 9` are not used in
that right-side calculation. This supports the following **unproved interface
targets**, rather than a new constant-band normalization theorem:

1. For arbitrary finite natural coefficients, `c ≤ 18` implies
   `overflow c (stripSuffix c B) = overflow c B`.
2. Alternatively, for arbitrary phase `c`, `Bounded B` implies the same equality.
   For `c ≤ 18`, use the first route. For `c > 18`, bounded `B` contains no `c`,
   so its suffix decomposition has zero removed letters.
3. For any original `State s`, **`Bounded s.B` alone** implies
   `overflowBit (Agent116.CertificateExterior.stateOuter s) = gam s`.
   The bit bound is needed here because `overflowBit` is the indicator of a
   nonzero carry, not the numerical carry when that carry exceeds one.

These candidates require no `Phase`, evenness, nonneutrality, positive head,
nonempty word, maximal original trim, `Admissible0`, or realization premise.
The state-level result would apply to bounded rejected candidates as well as
accepted rows. The completed source scan found no equivalent exported
strip-carry theorem within the pinned coverage described below.

## Consumer endpoints and exact hypotheses

The published row projection is
`rowOuter cert i = Agent116.CertificateExterior.stateOuter (cert.st i)`.
The current source explicitly leaves the indicator/legacy-count comparison open:

```lean
Agent6.CertificateCoordinates.checked_row_weighted_balance
    (cert : Certificate) (hc : check cert = true) :
  sumPrefix (fun i => weightedPhase (rowOuter cert i)) cert.P =
    9 * sumPrefix (fun i => weightedReverse (rowOuter cert i)) cert.P +
    9 * sumPrefix (fun i => (overflowBit (rowOuter cert i) : Int)) cert.P
```

Acceptance supplies each listed row's bound directly from
`(check_sound cert hc).2 i hi`; only its `Bounded (cert.st i).B` conjunct is
needed for the proposed indicator identity. Existing `sumPrefix_congr` then
handles the finite sum, whose right side is definitionally:

```lean
Agent110.Accounting.totalGam (cert : Certificate) : Int :=
  sumPrefix (fun i => (gam (cert.st i) : Int)) cert.P
```

The prospective accepted-certificate endpoint therefore reads:

```text
sumPrefix weightedPhase(rowOuter) P
  = 9 * sumPrefix weightedReverse(rowOuter) P + 9 * totalGam cert
```

Its only external premise is `check cert = true`. The sum identity itself can
be stated more generally for any candidate with bounded listed `B` words,
including the empty sum; acceptance enters when invoking the existing closed
weighted balance.

The optional gain form is a substitution of the already exported theorem:

```lean
Agent110.Accounting.totalGam_eq_twice_gains
    (cert : Certificate) (hv : Valid cert) :
  totalGam cert = 2 * (totalG cert + totalH cert)
```

It changes the final term to `18 * (totalG cert + totalH cert)`. Neither this
substitution nor the count identification proves an overflow occurs or gives a
new period exclusion. Those are distinct mathematical obligations.

## Boundary controls to retain in eventual proof work

These values are direct hand reductions of the inspected definitions, also
identified independently by the runtime specialist. They have not been newly
executed or kernel checked in this census.

| Phase and raw word | Trimmed word | Raw gam | Trimmed carry | Trimmed overflowBit | Meaning |
| --- | --- | ---: | ---: | ---: | --- |
| `c=2, B=[20]` | `[20]` | 2 | 2 | 1 | Dropping coefficient bounds makes indicator equal carry false, even in a permitted phase. |
| `c=19, B=[19]` | `[]` | 2 | 1 | 1 | Unconditional structural carry invariance is false; comparing only bits misses this carry drift. |
| `c=18, B=[18]` | `[]` | 1 | 1 | 1 | Empty output must preserve incoming carry one; phase 18 can remain allowed. |
| `c=9, B=[9]` | `[]` | 0 | 0 | 0 | Neutral phase 9 can remain allowed for this interface. |

## Minimal existing dependency closures

`dependency-closures.json` records complete ordered closures, counted before any
new module is introduced:

| Scope | Imports sufficient from existing files | Existing modules |
| --- | --- | ---: |
| Raw normalizer or structural padding/carry interface | `OuterBridge`, `CoordinateThreshold` | 8 |
| Original `stateOuter` versus coordinate `overflowBit` | `CertificateExterior`, `CoordinateCycle` | 16 |
| Weighted row balance and legacy `totalGam` consumer | `CertificateCoordinates` | 18 |

The eight-module closure is `TemplateStep`, `ReturnCertificate`, `OuterFinite`,
`OuterBounds`, `OuterBridge`, `TARGET`, `ExteriorFactorizationProof`, and
`CoordinateThreshold`. The smaller normalizer correspondence should be reused
from its original module rather than copied into a newly named theorem.
The full consumer already imports all necessary coordinate, projection and
accounting sources. It needs neither `CertificateFilter`, `CertificateControls`,
the Agent2 charge package, nor the experimental PR107 source.

## Duplicate and ownership boundaries

The complementary export census covers every one of the 1,831 top-level Lean
paths at main `7b9e663b3c40aadfd7038f264729f6b7e3c7ce88` by exact source-blob
matching or direct reads, plus 31 distinct additional public contribution blobs.
It enumerated 105 branches and pinned 132 task records at coordination
`32b2f562b54f5d14ce0d45ed2fd5368fa8cd8004`. Scoped branch reads include Agent109
OuterBridge/OuterCompat, Agent216 ConcreteEdge, Agent1 PeriodicOuterStrip and
PR107 at the captured commit below. The additional source receipt contains 32
exact captures, including the separately scoped branch source.

No equivalent native `overflow_stripSuffix` or `stateOuter` carry equality was
found. The newer Agent5 `stripSuffix_bounded` and `headD_stripSuffix` results use
the generalized integer model and do not establish this carry identity.
Unrelated preserved development, probe and audit attempts were excluded. This
is a bounded source census, not an assertion of theorem equivalence across all
branches. The parent owns the later main and guarded-claim delta checks.

- Agent109 owns the original norm/band/whole-template interfaces. This work should
  consume them, without another repeated-block normalizer or whole-word bridge.
- Agent110's `CertificateBudget.gam_eq_overflow` is the prior raw carry bridge;
  `Accounting.totalGam_eq_twice_gains` is already the exact gain theorem.
- Agent116 owns `stateOuter`, suffix normalization and the checker projection.
  A new carry-compatibility consumer must preserve those definitions and credits.
- Agent115's active task blob is
  `2b983584ad3afc50e21878fb2a882e2572d8037b`. PR107 targets high-rho recurrence,
  positive gain, a cycle telescope and mandatory overflow on closed exterior
  orbits. At directly captured commit
  `254b4bc6b545aa9dd027c7bb46e7c4022b5d2f27`, its target blob is
  `9485759ed79424207ca97fab3e8ad7a5c6b47e89` and experimental helper blob is
  `ecb978e22270787adacd4dbdd48b50519e14085c`. Its `gamma_eq_overflow` compares
  two `Outer` carry formulas; neither file imports or mentions the original
  checker `gam`, `State`, `Certificate`, or `stateOuter`. This census does not
  judge those experimental helpers to be accepted proofs.
- Agent110's active exact phase-six two-step return task remains separate,
  claim blob `486eb1460dab5cca752d312c623e2488c5d34ed4`.
- Agent216's General Int/Nat correspondence, Agent411's native charge map and
  generalized boundedness, and Agent412's modulo-three charge/interface/period
  results are distinct existing scopes. Their exact current claim blobs and
  exclusions are retained in `all-inspected-claims.json`.
- Agent6's current certificate claim explicitly says the normalized indicator
  must not be equated with `totalGam` without a proved bridge. Its inspected blob
  is `5d7c3811782d321cef05b1fee03f4daa30fb5d7c`. The parent decides and publishes
  the next guarded scope after the current review checkpoint.

The recommended next scope is therefore a narrowly attributed normalization-to-
accounting interface and its exact controls. It excludes a new rho recurrence,
overflow-necessity theorem, global cycle claim, period bound, accepting
certificate, or ordinary-integer realization result.
