# Independent RadixExterior review: accept its scoped conclusions

Reviewer: **Agent110 runtime/audit specialist, `/root/runtime_audit`**.
Review execution is separate from the `RadixExterior.lean` author. Additional read-only semantic reviewer:
`/root/runtime_audit/radix_semantics`; this helper did not compile Lean, run the author's
checker, or write files. The lead reviewer actually performed the rebuild and integer controls below.

Frozen source SHA-256:

`3aa5f400f939b7888a8e503cc1489514222701078449492f375681129c8e5716`

The parent supplied this remote reproduction pin during completion of review:
**`1cdc55c89b376faa270d1dffaf21e21b6eedeb4b`**, repository
`taco-jpg/p196-algorithm`; corresponding local commit:
`ee54c6e7d95cf9cd5d1a4bd530aa2773ac22f33b`, tree:
`a01ca07a2ff49f3dae2aa8dd97483e8e624915b8`。
Reproduction should pin that remote commit and check the source SHA-256 above. This review actually verified that
source hash and the recorded hashes of three dependencies. The reviewer performed no Git or remote operations.

No substantive mathematical error or incorrect conclusion scope was found in the15 new theorems. Accepted results concern
**insufficient information in the specific `(phase,Z)` observable and limitations on progress potentials based on it**.
They construct no exterior-state cycle, prove no global acyclicity, and establish no infinite-time conclusion about196.

## 1. Independent rebuild and axiom results

The lead reviewer reread and listed the actual dependency chain:

`Std → ExteriorCore → ExteriorCapTwo → ExteriorCoverage → RadixExterior`。

Previously absent `/workspace/scratch/63e10b24caf2/radix-review-build` was the sole
project LEAN_PATH. Four sources were copied bytewise from their original paths; every .olean was generated in that
empty directory, with no author .olean or dev-deps reuse. Runtime used the pinned
official Lean4.19.0 / commit6caaee842e94 with the explicitly recorded current-process readlink
adapter. Official compiler and standard library were unchanged.

| Module | Explicit public theorems | Other explicit public declarations | Compilation seconds |
|---|---:|---:|---:|
| ExteriorCore | 2 | 10 | 0.525 |
| ExteriorCapTwo | 3 | 0 | 29.146 |
| ExteriorCoverage | 5 | 1 | 0.926 |
| RadixExterior | 15 | 12 | 0.943 |

The independent scanner enumerated and checked all **48 explicit public declarations** across the four sources:
25 theorems and23 def/abbrev/structure declarations. It is not the author's checker; it uses fail-closed parsing
for the source syntax needed here and checks total declaration-token count.
Independent ReviewerAudit.lean queries every name's transitive axiom set exactly once.

All four compilations, version query, and complete axiom audit exited0. All48 results are present exactly once;
actual union is only propext and Quot.sound, without Classical.choice, custom
axioms, sorryAx, or Lean.ofReduceBool. Comment-stripped source also excludes sorry/admit,
native_decide, unsafe, implemented_by, and declaration-generating syntax. Every finite
decide equality/inequality witness in the new file is axiom-free.

All four originals and build copies were rechecked after compilation with unchanged hashes. Complete argv, environment, timings,
source/object/output hashes, all48 declaration results, and sign-off identity are in verification.json;
complete output is in logs/, independent source copies in source_snapshots/. rebuild.py is the actually
executed lead-review harness. This committed review directory contains no compiled binaries.

Finite enumeration in ExteriorCapTwo is only part of the existing Canonical definition's import chain.
This obstruction uses no cap-two enumeration conclusion; the rebuild cannot be promoted as a new width bound.

## 2. The map used is the original exterior update

The new file does not redefine advance. Unchanged ExteriorCore directly gives:

- `k = 1[c ≥ 10]`，`t = c − 9k`；
- `(D,e) = norm B 0`，`(E,γ) = norm (reverse B) k`；
- `u = c + e − 10k`；
- For γ=0, raw is `(D ++ [u]) + (reverse E ++ [t])`; otherwise it is
  `(D ++ [u]) + ([1] ++ reverse E)`；
- Next phase is2t and the next exterior word is raw with its maximal2t suffix removed.

These match the actual normalized exterior formulas in the original complementary-band description entry by entry.
Overflow is also the final carry of the same norm(reverse B)k, not a freely chosen carry.
Actual here means precisely that original deterministic map; the new Lean file does not newly prove a semantic bridge
for every ordinary integer and every gap.

For independent finite semantic checks, the lead reviewer wrote semantic_controls.py without importing the author's Python
program. It constructs three ordinary decimal integers with central phase lengths **9,10,17**, directly uses
integer addition and decimal-string reversal, and computes each new actual mirrored-sum digit word,
checking exterior, phase, constant center, and actual width increase. All **15 additions**
match the five-step exterior path below; full integers/words are in semantic-controls.json.
These are finite semantic controls, not a general bridge or infinite-safety proof.

## 3. Exact definition of Z and witnesses

value10 B=Σ Bᵢ10ⁱ, assigning the lowest exponent to the list's first entry;
`centeredValue c B = Σ(Bᵢ − c)10ⁱ`。
centeredValue_formula proves for arbitrary finite B:

`9 centeredValue c B = 9 value10 B − c(10^length(B) − 1)`。

Thus radixDefect is exactly the stated Z. Appending any number of phase letters c changes neither
centeredValue nor observable(c,Z); the induction omits no length or canonicality
hypothesis. Z may be negative; Int avoids natural-number truncation.

Independent hand calculations and integer controls both give:

| Time | Phase | Exterior word | Z | Next-step overflow |
|---:|---:|---|---:|---:|
| 0 | 6 | `[13]` | 63 | 1 |
| 1 | 12 | `[4,10]` | −252 | 0 |
| 2 | 6 | `[9,1]` | −423 | 0 |
| 3 | 12 | `[18,2]` | −846 | 1 |
| 4 | 6 | `[9,11,5]` | −423 | 1 |
| 5 | 12 | `[10,1,7,11]` | −14508 | Not used in the proof |

All six states have allowed positive even phases, coefficients in0..18, positive first coefficients when nonempty,
and final coefficients different from phase, satisfying original Canonical.

ReachedAfterOverflow s means there is a canonical ancestor a whose computed overflow is1,
and s is reached after finitely many further iterations starting from advance a. Using time0 as ancestor,
source/middle/endpoint require respectively1/2/3 further steps, giving correct witnesses.
The definition claims neither ancestry from196 nor an entire orbit staying indefinitely in a safe class.

Times2 and4 share only the observable. Their word lengths are2 and3, so the states differ strictly;
witness_not_state_return proves this separately in the kernel. Return of the table's observable
must not be called an exterior-state cycle.

## 4. Logic of the two main obstruction theorems

**no_autonomous_radix_factor: correct.** F must give the next observable for every state both canonical and
ReachedAfterOverflow. Source and endpoint are in that domain, both with input
observable(6,−423), but their successors are(12,−846) and
(12,−14508). One single-valued function cannot satisfy both. The theorem excludes only a uniform deterministic update
for this specified observable, allowing richer state information or a domain excluding these witnesses.

**no_overflow_strict_radix_observable: correct.** P depends only on the observable. The proof takes
the weak relation along source→middle and the strict relation along middle→endpoint,
whose actual overflow is1. Given mixed transitivity weak a b∧strict b c→strict a c,
the endpoints are strictly related; equal endpoint observables contradict strict irreflexivity.
No extra weak reflexivity, strict total order, or induction over arbitrary chain lengths is needed.
The integer-potential wrapper uses ordinary≤/<, proving required relation properties with omega, with correct scope.

It excludes the specified class of(phase,Z)-based potentials that **weakly increase at every step and strictly increase at every actual overflow**.
It excludes neither richer ordered information, additional carry memory, nor nonmonotone arguments,
and concludes neither existence nor absence of all exterior cycles.

radix_observation_is_order_sensitive correctly shows the observable is not universally reversal-invariant:
exchanging[1,5] and[5,1] can change Z. It does not claim injectivity on exterior states; the main counterexample
demonstrates precisely the insufficiency of that information.

## Review sign-off

**Reviewed-by: Agent 110 runtime/audit specialist (`/root/runtime_audit`)**

Additional read-only hand-calculation review: `/root/runtime_audit/radix_semantics`.
Sign-off concerns the frozen SHA-256 above and actual execution recorded here; this is a plain-text reviewer-identity statement,
not a cryptographic signature. Final verdict: **ACCEPT WITH STATED SCOPE**.
