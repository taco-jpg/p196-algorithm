# Independent semantic review of ModularSpan and ResidueOrbit

Reviewer: Agent111 digit-implementation subagent. Date:2026-10-15.

Conclusion: **no blocking defect found in mathematical semantics, hypothesis scope, actual-orbit connection, or dependency direction of the two targets at the pinned commit below.**

## Pinned version and execution boundary

Commit: `c3192d5bf2962298bcb2bb209a0947f657e8a7e5`, existence confirmed with `git rev-parse --verify`; targets/dependencies read through `git show <commit>:<path>`. SHA-256 values were computed from those exact returned bytes, not substituted live working-tree text.

| File | Pinned-commit source SHA-256 |
|---|---|
| `proofs/contributions/agent-111/exact-length-residues/ModularSpan.lean` | `1cad197771ad6a4a9577ac08d3e1a4afe143e354a96a261b8ebaa2c687c09754` |
| `proofs/contributions/agent-111/exact-length-residues/ResidueOrbit.lean` | `989e42134e6ae6c05775f569cc1b4cd916d0d45d5d87b6e471cbf3fe3e2cdfc6` |
| `proofs/research/Lychrel196Research.lean`, existing semantics/orbit-lemma dependency | `f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c` |
| `proofs/contributions/agent-111/exact-length-residues/Saturation.lean`, downstream file discharging conditional assumptions | `a638ff9844afa378dfe168feeaa8be372d2f2b5f6f3c1ff62ca5c2fe9f0685e0` |

This is **source and mathematical-semantic review**, without a Lean rebuild, relabelling previous compilation as independent execution, or replacing the environment specialist's fresh full build/axiom check. Another specialist wrote the targets; the reviewer changed neither mathematical file and performed no Git writes.

## ModularSpan: integer spans and bounded natural coefficients

`gcd_int_span` constructs integer Bézout coefficients for all natural m,n. The m=0 branch uses(0,1), including n=0; otherwise recursion on strictly smaller n%m uses n%m+m*(n/m)=n to convert coefficients to(y−x*(n/m),x). Subtraction is in Int, allowing negatives rather than truncated natural subtraction. Recursion follows `Nat.gcd_rec`.

The only substantive condition of `gcd_three_int_span` is gcd(q,gcd(c0,c1))∣a. It spans the outer gcd, then gcd(c0,c1), and multiplies by divisibility witness k, giving exact integer equality u*q+x*c0+y*c1=a. It assumes neither the desired modular combination nor unknown Bézout coefficients. Even with all three generators zero, divisibility permits only a=0, avoiding an unconditional arbitrary-target span.

`modular_span` explicitly returns **natural** coefficients: `∃ x, x<q ∧ ∃ y, y<q ∧ ...`, with q:Nat fixing their type. Integer coefficients are reduced by Euclidean remainder, then converted with toNat:

- hq:0<q gives a positive, nonzero integer modulus.
- `Int.emod_nonneg` makes the remainder nonnegative, so toNat loses nothing; hX/hY explicitly prove conversion back to Int equals that remainder.
- `Int.emod_lt_of_pos` gives converted natural coefficients strictly below q.
- Removing u*q from the integer equality gives the target residue; replacing both coefficients by their residues preserves it.
- Injectivity of Nat→Int and modulo-conversion theorems return the natural residue statement. The right side is a%q, not an erroneous demand that unreduced a be below q.

Boundary checks: q=0 is excluded by positivity in the bounded-coefficient theorem; q=1 is valid and forces coefficients0,0; a=0 is valid; zero c0 or c1 is not excluded; with both zero, the gcd condition is exactly q∣a. Only sufficient spanning is proved; comments/statements do not mislabel it an unproved iff.

## ResidueOrbit: object semantics and necessary conditions

The file imports only `Lychrel196Research`, using core `Lychrel196.orbit`, `step`, `reverse10`, `Palindrome`, `DecimalDigits.Canonical`, without an alternative orbit or weakened palindrome predicate. In the pinned core:

- `step n = n + reverse10 n`。
- `orbit n 0 = n`，`orbit n (k+1) = step (orbit n k)`。
- Palindrome p is ordinary finite-natural reversal equality reverse10 p=p.
- Canonical p d L requires L>0, every digit≤9, nonzero highest digit, and actual value d L=p.

By definition the orbit continues after any earlier palindrome; no finite first-palindrome stopping sequence is silently substituted.

`palindrome_not_dvd10` uses the reversed units digit equalling the original highest digit and reverse10 p=p to prove p%10≠0, with highest-digit positivity from the same Canonical witness. `even_palindrome_dvd11` uses exact-length reversal modulo11 to prove even-length palindrome divisibility. It uses the established 11∣99 case, not an assumed autonomous reversal law for every modulus.

When `palindrome_residue_compatible` transfers necessity along p%M=a%M, `Nat.dvd_mod_iff` is used only for factors proved to divide M: assumed10 for the first condition and gcd(M,11) for the second. Equality modulo M is not treated as equality modulo arbitrary other moduli. a need not be reduced; M=1 and a=0 are included. Necessity itself permits M=0 because modulo0 returns the original number; this is a valid conditional statement, not saturation existence modulo0.

`Compatible` contains exactly two necessary restrictions. `SaturationAbove` defines a property yet to be proved: above one threshold, each exact width and compatible residue has a positive actual palindrome. Sufficiency in `palindrome_residue_iff_of_saturation` explicitly uses supplied hs; necessity uses the prior conditions. A definition is not passed off as an unconditional theorem.

## Actual-orbit connection, positivity, and time range

`orbit_matches_palindrome_of_saturation` assumes hn:0<n and invokes pinned core `AstraModular.large_width_compatible_residue M n B hn`. It returns Canonical for the same actual orbit n t, B≤L, time bounds6+4*B≤t≤7+4*B, and compatibility of its actual residue.

Tracing that core interface's direct proof chain confirmed:

1. `large_width_compatible_state` starts from actual digits of a positive seed, combining `late_compatible_state` and `DecimalWidthGrowth.numeric_width_bounds`.
2. `numeric_width_bounds` includes Canonical(orbit n K)e W, not merely abstract length, with semantics from existing `iterPairs_representation`.
3. Late compatibility follows from actual-orbit divisibility by11 after step6 and impossibility of consecutive zero units digits.
4. `large_width_compatible_residue` only transfers divisibility/nondivisibility to residues modulo M, invoking neither palindrome saturation nor this contribution's main theorem.

The hs invocation targets exactly a=orbit n t%M with matching compatibility. From p%M=(orbit n t%M)%M, `Nat.mod_mod` and symmetry give the claimed orbit n t%M=p%M. Both returned Canonical witnesses use the same L, one for the orbit state and one for the constructed palindrome; neither digit functions d,e nor numbers are conflated. Only equal width/residue is claimed, not equality to p or eventual palindrome occurrence.

## Set conclusion: nonemptiness, positivity, and two thresholds

Nonemptiness in `closed_saturated_contains_palindrome_of_saturation` is ∃n,0<n∧S n, stronger than allowing only zero. hclosed requires forward closure only for positive members. Induction starts from that positive seed and uses core `orbit_positive n hn k` at each step, satisfying every positivity premise without assuming closure over all naturals or misusing{0} as a target counterexample.

`SetSaturatedAbove S M C` requires equal membership for actual canonical decimal numbers with equal width/residue within each L≥C. Different lengths may use different residue sets; no unnecessary condition is imposed on0 or objects lacking canonical representation.

Palindrome threshold B and set threshold C come from separate existence assumptions. The proof raises the first to max B C before finding an orbit state, satisfying both and avoiding application of eventual set properties to short lengths. After deriving S(orbit n t), the forward .mp direction of S(orbit n t)↔S p gives S p, retaining p>0 and actual Palindrome p.

## Noncircularity and evidence limitations

| Module/interface | Source of assumptions | Target conclusion left assumed or used circularly? |
|---|---|---|
| ModularSpan | Std only; Euclidean algorithm and divisibility | No saturation, orbit, or palindrome assumptions. |
| ResidueOrbit necessity | Actual core reversal, canonical digits, supplied palindrome | Derives restrictions from a witness without invoking sufficiency. |
| ResidueOrbit matching/set directions | Explicit SaturationAbove or existence assumption plus core orbit facts | Conditionality remains visible; existence is not fabricated here. |
| Pinned core orbit-compatibility interface | Actual digit growth, modulo11, and units-digit facts | Core imports only Std, not this contribution in reverse. |
| Downstream Saturation.exists_saturation_bound | Modulus decomposition, positive period, outer block, weights, span, position pools, CRT | Constructs saturation separately before discharging corollaries; does not prove itself using set or orbit-matching conclusions. |

A limited text scan of the two pinned targets found no `sorry`, `admit`, `native_decide`, or custom axiom declaration. This is source inspection, not Lean's transitive axiom audit. Cite the environment specialist's independent result for the complete build, executable evidence, and axiom closure.

No target statement needing repair was found. Tracing direct core interfaces confirms this contribution's actual semantics and noncircular dependencies; it is not a new independent audit of every proof in the existing core's more than4,000 lines.
