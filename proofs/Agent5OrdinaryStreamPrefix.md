# Agent #5: ordinary one-step paired prefix from coordinate streams

This package connects the published literal coordinate streams to the original
ordinary digit operation. It proves the exact first `B.length + 1` coefficients
of `paired (reverseAddDigits D)`, then combines that identity with the original
decimal-digit, positive-last-digit, 和 numerical-value theorem.

The mathematical source consists of two modules 和 six public exports in
`Agent5.OrdinaryStreamPrefix`. The complete source-pinned dependency closure has
fifteen modules. The corresponding registry is
`proofs/Agent5OrdinaryStreamPrefix.registry.json`.

## Exact statement

Let `D`, `B`, 和 `W` be finite lists of natural numbers, let `c` be one of
`[2,4,6,8,10,12,14,16]`, 和 assume every entry of `B` 和 `W` is at most 18.
The original shape hypothesis is

```lean
paired D = surrounded B c gap W
```

where the existing definition is exactly

```lean
B ++ List.replicate (gap + 2) c ++ W ++
  List.replicate (gap + 2) c ++ B.reverse
```

There is no additional lower bound on the natural parameter `gap`: even
`gap = 0` supplies two copies of the phase on each side of the middle word.

Write `n = B.length` 和 let the final carry selector be

```lean
if 9 * 10 ^ n ≤ rhoNum c B then 1 else 0
```

The principal structural endpoint is:

```lean
theorem ordinary_raw_prefix_from_streams
    (D B W : List Nat) (c gap : Nat)
    (hc : nonneutralPhase c)
    (hB : Coefficients B) (hW : Coefficients W)
    (hshape : paired D = surrounded B c gap W) :
    (paired (reverseAddDigits D)).take (B.length + 1) =
      List.zipWith Nat.add
        (adicNumeratorDigits (B.length + 1) (zValue c B - (c : Int)))
        (fractionDigits (B.length + 1) (rhoNum c B)
          (9 * 10 ^ B.length *
            10 ^ (if 9 * 10 ^ B.length ≤ rhoNum c B then 1 else 0)))
```

The low stream uses a signed numerator over 9; its digit rule uses Euclidean
remainders. The high stream uses ordinary fractional long division. Each stream
consists of decimal digits, while their coordinatewise sums are **paired
coefficients** 和 may exceed 9. The left side is the prefix of the paired output
word, not the prefix of the output digit word itself.

The companion quotient endpoint replaces the selector with
`rhoNum c B / (9 * 10 ^ B.length)`, using Agent #6's existing theorem.

## Ordinary numeral interpretation

The wrapper `ordinary_reverse_add_from_streams` adds the original assumptions
`DecimalDigits D` 和 `PositiveLast D`. Its four conclusions are:

1. `DecimalDigits (reverseAddDigits D)`;
2. `PositiveLast (reverseAddDigits D)`;
3. `numeral (reverseAddDigits D) = numeral D + numeral D.reverse`;
4. the threshold-based paired-prefix identity above.

The existing `numeral` reads a list in little-endian order. Thus `PositiveLast D`
requires a positive most significant digit. A zero least significant digit is
allowed: `[0,1,1,2]` represents 2110 和 takes one ordinary step to 2222.

The proof obtains the first three conclusions directly from
`P196.Agent6.reverseAddDigits_correct`. It does not reprove value conservation.

| Assumption or boundary | Structural prefix | Ordinary numeral wrapper |
|---|---|---|
| Eight original nonneutral phases | Required | Required |
| Original `surrounded` shape | Required | Required |
| Entries of `B` 和 `W` at most 18 | Required | Required |
| `DecimalDigits D` | Not assumed | Required |
| `PositiveLast D` | Not assumed | Required |
| Empty `B` or `W` | Included | Included when the other hypotheses hold |
| Zero coefficients or untrimmed `B` | Included | No extra trimming premise |

For nonempty `B`, positivity of its first paired coefficient already follows
from a canonical positive-last input 和 the shape. A zero-head nonempty `B`
can occur in the structural theorem with a leading-zero input word, but cannot
satisfy all the canonical wrapper hypotheses. This distinction is retained.

## Proof reuse 和 attribution

| Export | Role |
|---|---|
| `normalize7_eq_norm6` | Identifies the two original Nat normalizers, including their terminal carry. |
| `nonneutralPhase_nonneutral6` | Converts the existing eight-phase predicate to the original ordinary projection domain. |
| `ordinary_raw_prefix_from_normalized_streams` | Substitutes the proved low/high stream identities at tail length zero into the original raw projection. |
| `ordinary_raw_prefix_from_streams` | Uses the exact coordinate threshold for the final carry. |
| `ordinary_raw_prefix_from_streams_quotient` | Uses the exact coordinate quotient for the final carry. |
| `ordinary_reverse_add_from_streams` | Bundles the paired prefix with the original ordinary value 和 canonical-digit conclusions. |

The main input is `P196.Agent6.surrounded_raw_exterior`. Original Agent #6
sources are imported unchanged through `ExteriorCore`, `ExteriorBridge`,
`ExteriorProjection`, 和 `ExteriorArithmetic`. The five Agent #5 coordinate
modules remain frozen at source commit
`fff2ca0a7ecbb2ee50eccf4cdc80f07b274e50e2`, with their final evidence published
at `5bbd70c486b3c274cfc9bf244cc92e551419d5d8` in PR #97.

Agent #6's coordinate threshold is the unchanged blob
`34ddc74962d8bbef954f1626a80593de60906215`. The adjacent historical
`Agent109.Outer.normalize7_eq` has `Agent109.norm` as its target; it is not
misidentified as the direct Agent7/Agent6 adapter proved here.

The full source identity 和 authorship record is in
`contributions/agent-5/ordinary-stream-prefix-20261016/PROVENANCE.json`.

## Verification

Both new modules compiled on their first author attempts with Lean 4.19.0
`--trust=0 -j1 -DElab.async=false`. The two genuine author specialists retained
their commands, source identities, dependency records, 和 axiom logs.

A separate non-author specialist reviewed all six statements, inherited
thirteen explicitly source-hash-recorded dependency objects, freshly compiled
the two new modules, 和 ran a complete fifteen-origin audit. All three strict
commands passed. The audit covers 267 theorem declarations 和 all six new
exports. Their mathematical dependencies use only `propext`,
`Classical.choice`, 和 `Quot.sound`. Three generated implementation declarations
are separately inventoried 和 absent from those mathematical dependencies.
This review is not represented as a fresh fifteen-module dependency build.

The independent receipt SHA256 is
`3c08d98fb198270d4a347f34818ab3b2454060eb2102750a3851a5663c56466c`.
The semantic review SHA256 is
`785fc91fcc3c1a005a4c272ae429c25020f2b256cd3a019e36f74eb64ca4922f`.
The complete review 和 all retained source/log files were rehashed after a
shared storage incident; all matched. Only a reproducible public runtime
download was removed to reclaim space. Source 和 compiler evidence were kept.

The parent then rebuilt all fifteen modules from the exact published source
`5b4238ebe95f5fb80512d1b1ad3dbe3b062279a3` into a new empty output directory.
All sixteen module/audit commands exited zero. The complete audit again found
267 theorem declarations, six fixed exports, 和 only the three standard theorem
axioms. The receipt records `source_tree_clean=true` 和 has SHA256
`742937cdfcc106812ef4cfb24652cbc7462b4b3e406be0e26e25652617e4ceea`.
The exact report, all sixteen logs, generated audit source, 和 file manifest are
retained under `verification/canonical-published-source/` in this contribution.

The unchanged verifier retains its original Agent #1 author metadata. The
top-level report names the actual Agent #5 parent executor. Final publication
adds evidence 和 metadata while keeping every mathematical source unchanged.
The source PR is #121, stacked on prerequisite PR #97.

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent5OrdinaryStreamPrefix.registry.json \
  --project agent5-ordinary-stream-prefix \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/new/agent5-ordinary-prefix-check
```

## Boundary controls 和 scope

The independent finite controls cover 64,008 coefficient-word cases, 51,984
canonical ordinary realizations, 和 384 longer patterns. They are finite
diagnostics, separate from the quantified Lean theorems.

Three controls clarify the actual assumptions:

- With `c = 2`, `B = []`, `gap = 0`, `W = [18]`, 和 canonical
  `D = [1,1,9,1,1]`, the required one-coefficient prefix is `[4]`.
  The next actual paired coefficient is 5, while the next stream sum is 4.
  A longer raw prefix therefore needs its own proved condition.
- A hypothetical band of only one phase column gives `D = [1,9,1]`:
  the next paired prefix is `[5]`, while these exterior coordinates give `[4]`.
  Such a shape is excluded by the actual `gap + 2` definition.
- The leading-zero word `[0,1,1,1,1,0]` satisfies a structural shape but
  violates `PositiveLast`. Literal fixed-word reversal gives a sum of 22220;
  ordinary reversal of the represented integer 11110 gives 12221.

The theorem concerns one ordinary step under the stated input shape. No claim
is made that this shape persists along an orbit. It does not establish an
all-time safe orbit, an exterior no-cycle theorem, or a conclusion about 196.
Agent #4's spacer/specialization work, Agent #16's mod22 bridge, Agent #216's
general Int/Nat bridge, 和 the separately owned cycle questions remain separate.

Ownership was accepted before implementation at coordination commit
`e981de251ef29b24578dfe8bd79cdd2ba36c24f4`; task
`agent5-ordinary-raw-prefix-streams-20261016`. Public coordination is issue #61.
Agent #5 holds no main integration slot.
