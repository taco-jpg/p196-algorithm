# Independent replication review of Agent112 automatic_admissibility

**Conclusion: accept the conditional theorem at this pinned source; no circular canonicality assumption or omitted zero-head branch was found.**

Lead reviewer: Agent110 runtime/audit specialist, `/root/runtime_audit`.
Additional read-only semantic reviewer: `/root/runtime_audit/radix_semantics`.
Agent112 authored the three mathematical sources; this directory records independent replication, rebuilding, and review,
not mathematical attribution to Agent110. The author's checker was neither executed nor reused.

Original remote source is pinned in `taco-jpg/p196-algorithm` at commit
`e7689d35f41ff325037a238cfc594d95e0da04e1`。
Review task-claim commit: `a13bd7cfbe0d5a412b6b11645ccbe3a753ed52eb`.
Only read-only `git show`/`git rev-parse` inspected pinned objects already fetched by the parent. The reviewer performed
no Git writes or remote operations and changed none of Agent112's originals.

## 1. Exact snapshot and actual execution

The three files in `source_snapshots/` are byte-identical to originals at that commit:

| Module | SHA-256 | Git blob SHA-1 |
|---|---|---|
| AdmissibleCenters | `7a7b9791e04994c8050606f211cac34b938ce8b63fa723ff54374c25eea97210` | `6366eaf4f5d16a8a1a999e7474c44239111e83e7` |
| SymbolicGrowth | `e1d125447143027920fefc0ce2106b01052cc10ba9ff07e94c8f6a312622b4f8` | `e6ea91c07f9600df656cd6d8193623ce34c659c1` |
| AdmissibleHeads | `696bb4cca62a931738ffd837c95a89daeaf74056d35f1e6c38755120ea56ef65` | `0754d027159fef059efc38a9692d4edf278c0039` |

`PROVENANCE.json` also records original paths, byte counts, and snapshot paths. Dependencies come from the same pinned
commit, without mixing newly changed working-tree files.

Actual newly created, initially empty build directory:
`/workspace/scratch/63e10b24caf2/agent112-review-build`。
Complete local dependency chain independently checked from imports:

`Std → TemplateStep → ReturnCertificate → AdmissibleCenters → SymbolicGrowth → AdmissibleHeads`。

Only five project sources are compiled; no `AdmissibleCompat`, `Targets`, or author objects are imported,
and no `.olean` files from `dev-deps`, previous reviews, or other agents are reused.
Official Lean4.19.0, release commit `6caaee842e94`, runs with the already published, hash-pinned
current-process readlink adapter; compiler and official library bytes are unchanged.
Every invocation uses `-j1 -DElab.async=false`; project `LEAN_PATH` contains only the new directory.

| Module | All public theorem/lemma declarations | Compilation seconds |
|---|---:|---:|
| TemplateStep | 52 | 5.703 |
| ReturnCertificate | 17 | 3.055 |
| AdmissibleCenters | 10 | 0.891 |
| SymbolicGrowth | 6 | 0.570 |
| AdmissibleHeads | 14 | 1.524 |

All five compilations exited0. `AllTheorems.lean` was then actually executed, querying transitive axioms for all
**99 public theorems**, requiring each expected full name exactly once, without omissions or unexpected
names, including dependency theorems ending in apostrophes. Agent112's three files contain **30 theorems**.
Every result uses only a subset of `propext`, `Classical.choice`, and `Quot.sound`.
After stripping comments/strings, none of the five sources contains sorry/admit, custom axiom,
native_decide, sorryAx, ofReduceBool, unsafe, or implemented_by.
The reused Agent105 declaration scanner is explicitly identified and hashed; it is not
Agent112's checker and rejects unsupported declaration syntax.

Original source, exact snapshots, build-source copies, and compiled objects have SHA-256 records; all three snapshots were
rechecked after compilation and unchanged. `verification.json`, complete `logs/`, the actually executed
`rebuild.py`, and generated `AllTheorems.lean` preserve all evidence.
Counts measure audit coverage, not new mathematical discoveries.

## 2. Original targets and dependency interfaces were not replaced

The full meaning of `automatic_admissibility` is:

```lean
∀ cert : Agent109.Cert.Certificate,
  Agent109.Cert.check cert = true →
  ∃ H M, Agent109.Cert.Admissible0 cert H M
```

`Admissible0` uses the original `ReturnCertificate.lean` definition, not a weaker replacement.
It says exactly that initial C is `H ++ M ++ reverse H`, length M≤1, every coefficient of M
is even, and initial B has positive first coefficient whenever nonempty.

`check_sound` gives original `Valid`: a nonempty certificate state list, with original
`LocalOK` at every cyclic index. This includes phase, coefficient bounds, exact raw-block trimming equations, nonpalindromicity,
and continuable gap lower bounds; it does **not** include central reflection, positive head, Canon, or integer realizability.
The new proof does not quietly add these desired conditions back into Valid.

The lead reviewer read every proof in all three new files section by section and cross-read original interfaces:
`LocalOK`/`Valid`/`check`/`Admissible0`, the original existence bridge, and
`stepWord`/`normalize`/`norm_template`/`stepWord_template`、`LastPos`、
`canon_normalize` and `evalL_norm`. The discussion below explains the actual logical role of each proof segment.
This does not claim a new statement-by-statement semantic review of every other repository theorem.

## 3. AdmissibleCenters: predecessors force a valid center

1. `pair_wrap` separates the paired endpoint sum; strong induction on word length in `pair_mirr` proves every
   pair w satisfies original Mirr. Base cases include empty/singleton words; a singleton pairs to a+a,
   so its central coefficient is even. Symmetry of w is not assumed.
2. `mirr_unwrap` removes one equal-endpoint layer from a Mirr word; `mirr_trim` removes k
   pairs of equal phase coefficients. k may be zero and trimming need not be maximal.
3. `raw_center_mirr` checks both carry branches of original Cr; each is the pair of a word,
   hence unconditionally Mirr.
4. `valid_center_mirr` constructs a predecessor j for every cyclic index i: P−1 when i=0, using P>0,
   otherwise i−1. LocalOK's exact Cr trimming equation and step2 imply target C is Mirr.
   The self-predecessor at P=1, empty center, and singleton center are covered.
5. `mirr_split` directly extracts H/M from Mirr's constructors; `valid_center_split` applies it.
   At this stage `admissible_of_valid_head` still explicitly requires initial positive head, honestly eliminating only
   the center condition. `certificate_existence_of_head` retains that same explicit head assumption.

This segment does not derive center shape from an integer orbit of a certificate not yet realized; it uses only actual
raw-center pair structure and predecessors on a finite cycle.

## 4. SymbolicGrowth: strict growth without canonicality

For lists of Nat coefficients, `evalL_pos_iff` equates positive value with existence of a positive coefficient; thus
`evalL_reverse_pos` needs no positive first/last entry. `stepWord_value` uses value addition for equal-length zipAdd
and original `evalL_norm` to obtain

`evalL(stepWord w) = evalL w + evalL(reverse(normalize w 0))`。

If evalL w>0, normalization and its reversal remain positive, so `stepWord_strict` gives strict growth
for any such symbolic word. No equality is inferred from canonical-digit representation, and highest-end zero columns
are allowed: noncanonical `[0,1,0]` has value10 and updates to `[0,2,0]`, value20,
consistent with the argument. This illustrates the boundary, not an extra large-scale validation.

The `bounded_evalL` bound is exact: with every coefficient≤18,
evalL w+2≤2·10^length(w), matching the geometric sum attained by an all-18 word.
`no_bounded_width_orbit` gets value at least k at step k from strict Nat growth; taking
k=2·10^L contradicts the bound at fixed length L. It requires constant symbolic-list length,
including possible highest-end zero columns, without borrowing canonical integer digit-length properties.

## 5. AdmissibleHeads: the zero-head branch and noncircularity

### Conditional propagation of a positive head

`pair_preserves_lastPos` and `stepWord_preserves_lastPos` prove that a bounded word with LastPos
retains LastPos after actual stepWord. The latter does use `canon_normalize`,
but its LastPos assumption is explicitly supplied in this **conditional implication**.

`template_head_of_last` recovers B's head from reverse B at the template's end.
`local_symbolic_step` derives one-step template equality only from LocalOK's phase, bounds, exact raw equations,
and gap lower bounds; original `stepWord_template` explicitly requires neither symmetry nor
positive head. `local_headPos` combines these into
HeadPos s.B→HeadPos s′.B without assuming its conclusion.
`cyclic_headPos` propagates the conditional along the nonempty finite cycle to any specified index.

### Empty B is not confused with a zero head

HeadPos w:=∀x,w.head?=some x→0<x is vacuously true for empty B.
Thus ¬HeadPos B requires nonempty B=0::E and excludes empty B.
The nil branch of `gamma_zero_of_not_head` explicitly gives a contradiction; the cons branch uses
a nonzero natural being positive to show the head is zero. Reverse normalization processes that zero last with incoming carry≤1,
so final carry must be0.

This distinction matters: empty B may have actual gam s=kOf s.c=1; source does not
misclassify it as a zero-carry case. Highest-end zero coefficients are not silently trimmed;
original normalize preserves same-length norm output and appends a column only for nonzero final carry.

### A purely symbolic invariant completes the contradiction

`WordInv` records only a template at some cyclic state and G/H satisfying lower bounds; it contains no positive head, central
reflection, Canon, ordinary-integer realization, or admissibility.

- `wordInv_step` preserves WordInv using LocalOK's exact formula; G/H may change.
- `wordInv_bounded` derives whole-word bounds from the corresponding cyclic state's original coefficient bounds.
- `wordInv_pos` obtains a positive coefficient from a nonempty phase band with c≥1 and G≥lo≥2,
  not from positive head.
- Assuming every cyclic state fails HeadPos, `wordInv_same_length` uses actual gamma=0 above, `norm_template`,
  norm length, and pair's equal-length property to prove one-step length preservation,
  without assuming individual B/A/C lengths or G/H stay constant.

`valid_headPos` supposes failure at one index. Success elsewhere would propagate there by cyclic_headPos,
a contradiction, so every index fails. Initial state and actual lower bounds then construct purely
symbolic WordInv and preserve it for all k. The orbit is positive-valued, bounded, and fixed-width, contradicting
the previous file's strict-growth theorem.

**Canonicality therefore occurs only in the local implication that an already positive head stays positive; the failure branch
proving all heads positive invokes neither integer realization, admissibility, nor an existence conclusion.**
This dependency direction is noncircular.

## 6. Final conclusion and explicit boundaries

`automatic_admissibility` first obtains original Valid from original check, invokes proved
valid_headPos, then reconnects center splitting, eliminating every additional assumption in original Admissible0.
`certificate_existence_of_check` invokes the original conditional existence bridge, concluding:
**If check accepts a certificate, some integer has an entirely nonpalindromic orbit.**
It supplies no accepted certificate, proves no certificate must exist, and does not identify the integer as196.

No failure example or larger enumeration needed to be invented: the target is a universal proof; complete five-file
compilation and per-declaration axiom checks succeeded on the first attempt. Boundary checks use the preceding reasoning and original definitions.
Future consumer wrappers should cite only these three exact source snapshots and use original check/Admissible0;
independent review of new wrappers and their closure is a next step, not endorsed in advance here.

## Review sign-off

**Reviewed-by: Agent 110 runtime/audit specialist (`/root/runtime_audit`)**

Additional read-only semantic review: `/root/runtime_audit/radix_semantics`.
Conclusion: **ACCEPT — exact-source independent rebuild and scoped semantic review**.
This is a plain-text reviewer-identity sign-off, not a cryptographic signature. It covers only the pinned commit/hashes and
actual execution in verification.json. Mathematical authorship remains Agent112's.
