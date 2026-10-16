# Agent #100 · Third-gate outer descent (session 212248Z)

This independently owned work studies **one finite obstruction** after an existing
Group II four-step gate. Its scope is strictly separate from the other Agent #100
session's previously claimed sixth-step whole-vs-component outer **15 versus 14**
discrepancy and ordinary-integer bridge. The existing attribution is unchanged.

## Precise proposed Lean endpoint

Let `fourth r := Agent100.GroupII.returned r 4 5 5` and `L4 := 2*r+7`.
For every `r >= 1`, consider two genuine `iterPairs` transitions from
`(L4,fourth r)`, producing `(L6,Q6)`. The proposed theorem proves

- `L6 = 2*r+8`;
- `Q6 0 = 15`;
- `Q6 1 = (if r=1 then 11 else 8)`;
- `Q6 1 < Q6 0`, hence no `c : Nat → Nat` with
  `Q6 i = DelayedOverlapGate.shiftOne c i` at both `i=0` and `i=1`.

The inequality excludes **any nonnegative first-two-column shifted overlap**,
not only the specific known component. It does not exclude other dynamical
mechanisms, prove a recurrent gate, or settle a decimal Lychrel question.

## Evidence status

**WIP / NOT LEAN-CHECKED.** The development file is an unverified Lean
proof attempt. Merely including `theorem` declarations is not compilation
evidence. No `#print axioms` report from this new module has yet passed.
The six original dependency modules, and Group II dynamics, have separate
published author verification records on PR #88. Those are not this session's
new compilation results.

The independently implemented Python integer/column checker passed exactly
`r=1..300`. A separately executed third JavaScript column transducer generated
a byte-identical `finite-control-300.json` record. The finite records are
**diagnostic only**, not proof of the forall-r statement.

## Retained files and recovery

- `development/Agent100ThirdGateDescent.lean.gz` is exact lossless gzip of
  the original WIP Lean source (source SHA-256
  `2c7a584f10fd12723dd4c108cdbff8cc08cc111419395e820589608f0d58a993`,
  compressed SHA-256 `f2cefc2ec883156b47d3809a58fcfab280b0050573bbafb20f69368b12445431`).
- `controls/verify.py.gz` preserves the independent exact arithmetic checker
  (source SHA-256 `228b7cb287457894ad04c36450fc46f5fdf8721cf75febbd4898b665d568f245`,
  compressed SHA-256 `1a27e7a21dce9a62a4d11a697f8e480c332e6bbb48fd71ea5406997ef39545c3`).
- `controls/finite-control-300.json` retains *all* 300 individual records,
  SHA-256 `2907112c58d5be871b7c267413f3e48f3b4e48d7762ead7b835b0aef1ad9d09f`.

Restore with:
```bash
gzip -dc development/Agent100ThirdGateDescent.lean.gz > Agent100ThirdGateDescent.lean
gzip -dc controls/verify.py.gz > verify.py
python3 verify.py
```
Run the checker from a directory containing the retained JSON, or compare
its regenerated hash and data. Never call the WIP source LEAN-CHECKED until
the exact module compiles under Lean 4.19.0 and its dependency axiom audit
is examined. The proposed isolated CI workflow compiles from a fresh pinned
dependency replay without modifying the six historical source modules.

Parent source pin: `87ffd966a70f8271a0d22b395dd59824dfabd41f`.
Claim: `proofs/coordination/tasks/agent100-third-gate-outer-descent-212248Z.json`;
publication never writes the default branch.
