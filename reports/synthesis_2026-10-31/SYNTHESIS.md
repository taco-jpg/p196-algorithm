# Consolidated Lychrel synthesis findings — 2026-10-31

User-requested publication of the important findings from five separate 2026-10-31 proof-synthesis audits. Repeated claims were consolidated; source references 和 limitations are retained.

**Decimal existence remains UNDECIDED. No explicit positive decimal integer with a proved infinite palindrome-free orbit was recovered.** The useful outcome consists of sharper missing hypotheses, recovered stronger results, invalid joins, 和 concrete corrections.

Publication source checks used main `95edd48c10119b35ba9d4775d790f815596afde3`. The underlying audits mostly use frozen `40d775ff9bfe1cd8e9f38137f026176af4427501`, with separately documented later deltas. A corpus inventory does 不 amount to verification of every proof.

## 1. Stop duplicating already-solved certificate interfaces

[Agent112.Admissibility.checked_positive_decimal_seed](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/lean/P196/Drafts/Agent112CertificateAdmissibility/AdmissibleCompat.lean) already states:

```lean
theorem checked_positive_decimal_seed
    (cert : Agent109.Cert.Certificate)
    (hc : Agent109.Cert.check cert = true) :
    ∃ m, 0 < m ∧ Lychrel196.IsLychrel m
```

Automatic admissibility, positivity, ordinary decimal semantics, 和 the time-zero nonpalindrome requirement are already handled for an accepted certificate. The substantive missing premise remains an actual accepted certificate.

[Agent208.CertificateBounds.structural_cycle_existence](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/lean/P196/CertificateBounds208/BoundSynthesis.lean) further reduces the original-format task to `StructuralValid cert` with `totalG cert >= 0` 和 `totalH cert >= 0`. Bound synthesis 和 local safety are already connected. These are sufficient formats; no equivalence with unrestricted decimal existence follows.

[Agent112.Eventual](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/lean/P196/Drafts/Agent112EventualRealizability/EventualCompat.lean) also handles one finite positive natural-coefficient word with all-time safety under the exact normalized symbolic dynamics. Initial symmetry 和 coefficient bounds need 不 be added to that theorem; an infinite spatial ray or a new word for each horizon fails its finite-word/all-time premise.

Verification label: existing formal statements, source-inspected during the audits; no fresh kernel replay in the publication pass.

## 2. The most concrete remaining T12 obligation

Use the phase-zero B34/W9 table in [lat_p12m9.txt](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt). Let U range over the 30 rotations of `(9,a,18-a)`, with even a from 0 through 18. Let J,C be finite coefficient words in 0..18, with C symmetric 和 an even midpoint when its length is odd.

```text
H(q,k) = B0 ++ W0^q ++ J ++ U^k
P(q,k) = H(q,k) ++ C ++ reverse(H(q,k))

Find admissible finite J,C,U satisfying
Phi^120(P(14,100)) = P(14,105).
```

`Phi` means the complete ordinary-decimal pairword successor, including both physical carry ports, overflow, the shifted high digit, 和 midpoint closure. Full endpoint equality matters.

[T12's proof](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/new_structures/T12/NOTES.md) already supplies:

1. A uniform return equivalence for all independent `q>=14,k>=100`.
2. The actual clock `(1000)^30` 和 an odd rooted pair coefficient at every intermediate phase.
3. Insertion identities permitting successive macro-boundaries `P(14,100+5r)`.

An admissible reference pairword has an explicit finite positive source: split each mirrored coefficient s into `s-min(9,s)` 和 `min(9,s)`; split an odd midpoint evenly. The outer coefficient 10 gives leading digit 9. Reference length: `920+2|J|+|C|`.

Together, one full return, the pumping argument, 和 the phase guard yield an infinite nonpalindromic orbit. Equality of pairwords suffices because a complete pairword determines the next ordinary integer; no assertion that an arbitrary digit splitter commutes with the macrostep is needed.

The composition already appears in [LEMMA_GRAPH](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/docs/LEMMA_GRAPH.md); the audits recovered 和 checked the connection, without supplying the missing witness. T12 remains PAPER PROOF with computational controls. A fully Lean-checked instantiation remains additional work.

[AC46](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/new_structures/AC46/REPORT.md) excludes C lengths 1..6 for **every finite J**, all 30 U, at the stated phase 和 widths (COMPUTED + PAPER PROOF). Empty C also falls into the excluded family: after lifting to k>=101, rewrite `U^k reverse(U^k)` with centre `U++reverse(U)` 和 k-1 outside copies. Thus the fixed phase-zero family needs a representative escaping these short-centre cases.

The width reduction bounds q,k for testing a proposed witness; it supplies no bound on |J| or |C|. The complete marked-fold 120-track physical product remains unbuilt/undecided in the cited sources. Small joined-column products 和 bulk SCCs do 不 decide its nonemptiness.

## 3. Two reproduced corrections requiring attention

- **[Y13 correction](Y13_CORRECTION.md) / #478:** `99*111=999*11=10989` refutes the broad repunit interval lemma. The proof drops `M_h/M_g`. The narrower actual charge-2 first-exit assertion remains unresolved by that counterexample; the existing broad argument fails to prove it. The dependent GAP_MAP restriction needs repair.
- **[Lattice boundary correction](LATTICE_BOUNDARY_CORRECTION.md) / #479:** a genuine 167→168-digit transition preserves every lattice coefficient below cut 79 while `(10,0)->(6,1)` 和 the actual/nominal descending carries differ. The old `latcell2.py` graph omits the edge. Its emptiness alone cannot establish the advertised universal physical exclusion.

Both correction reports contain standalone reproductions; [reproduce.py](reproduce.py) checks the counterexamples 和 port comparisons against [evidence.json](evidence.json). Fresh Python checks 和 independent JavaScript BigInt checks passed. Neither correction establishes a positive return or invalidates every later obstruction.

## 4. Scope distinctions that change the research map

| Finding | Supported conclusion | Remaining limit |
|---|---|---|
| [W9 bounded-centre obstruction](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/results/EdgeRelaxW9NoCentre.md) | Excludes bounded-width centres on the specified rooted p12/m9 lattice at every temporal period; COMPUTED + PAPER PROOF. | A growing U3 interior between W9 和 the midpoint violates the bounded-depth premise. T12 remains outside the exclusion. |
| [Recovered p11 obstruction](https://github.com/taco-jpg/p196-algorithm/blob/1f4ed4c5033754521c198506ad4b669232cad09f/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/persist_neutral_interface_exclusion.txt) | For its exact prescribed p11 clock/ports, strict descent excludes every finite symmetric initial centre sustaining the boundary forever, including growing 和 nonperiodic centres. | Specific p11 interface only. Finite graph premises are computational; the concrete theorem remains outside Lean. No p12/T12 consequence. |
| [Neutral no-cap report](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/reports/NeutralBandNoCapAllPeriods.md) | Known p11/p12/p22 streams have scoped cap/converter exclusions. | The blanket claim requiring a new exterior period >32 exceeds the cited [census](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/exterior_census/EXTERIOR.md), which explicitly retains capped words. Later results require matching coverage before removing an exception. |
| [Latest uniform-band result](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/results/UniformBandLeftEndsT24.md) | Current main reports all-height exclusions for uniform absorbing-band left ends with T<=24, except two T=24 tasks. | COMPUTED; the two stopped tasks, T>24, nonuniform bands, 和 arbitrary centres remain outside its conclusion. No fresh large census replay here. |

The p11 archive uses clock `11000100001` 和 ports `01001100111`. Both equal the displayed THEORY pair rotated left by one; the paired rotation was independently rechecked. Its potential `canonical width + (0 if first coefficient=14, else 3)` strictly decreases every 11-step block, given the listed finite-graph facts. Re-running those graph censuses was outside the publication pass.

## 5. Attractive positive pieces that do 不 yet join

**Scalar-nine centre renewals.** The eight [stored centre renewals](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/new_structures/Agent6NineRailCentreRenewal/cert.json) have primitive carry-word periods 8 or 16. The known neutral-p12 exterior carry word `101010010101` has primitive period 12. These periods were freshly recomputed. Rotation 和 repetition cannot make the infinite streams equal. A physical returning W9/J emitter could provide a different interface, but remains missing. Independent sources realizing separate centre edges do 不 provide one continuous returned orbit.

**W9 versus neutral 9-wire.** At coefficient 9, `floor((9+c)/10)=c`: a neutral wire transmits carry. W9 denotes a nonconstant nine-coefficient periodic band. The names do 不 identify interchangeable interfaces.

**P24 centre.** The concrete centre from [PR381](https://github.com/taco-jpg/p196-algorithm/pull/381) uses `(110001001000)^2`, overflow density 1/3. Known neutral p11 和 p12 densities are 4/11 和 1/4. Rotation 和 repetition preserve density; those particular components cannot join. Same-driver one-/two-lap exclusions remain limited to their proved scope.

**p8 lasso aliases 和 quotient lifting.** The audits match the archived [PR384](https://github.com/taco-jpg/p196-algorithm/pull/384) array to current [rec1](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/calculation/decimal_frontier/lattice_formats/p8_scc.txt) after temporal shift 7: the 39-column stem, 20-column loop, 和 448 inward-carry entries agree. Treat the records as aliases. An infinite spatial lasso lacks a finite terminal centre. Per-edge existential realizations also fail the generic quotient theorem's universal source-fibre lifting premise.

## 6. Retire vacuous routes 和 invalid proof shortcuts

- [DecimalUnboundedMass.not_constant_digitSum](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/lean/P196/Foundations/LychrelDigitSums.lean#L5232) explicitly negates the positive constant-digit-sum premise of an older conditional existence theorem. Conserved lattice charge differs from ordinary digit sum.
- [Fixed-finite-ensemble extraction](https://github.com/taco-jpg/p196-algorithm/blob/95edd48c10119b35ba9d4775d790f815596afde3/lean/P196/Drafts/Agent317M99C317Uniformity/UniformityBridge.lean) requires one fixed finite candidate set before every horizon quantifier. Fixed cardinality with horizon-dependent integers does 不 meet the premise.
- A complete safe language requires nonemptiness, an actual finite seed, exact successor closure, 和 palindrome avoidance simultaneously. Intersecting a closed-but-unsafe language with a safe-but-nonclosed language does 不 automatically preserve closure.
- Whole certificates in other bases validate formats without transferring their arithmetic to base 10. The recovered base-20 instance remains a base-20 result.
- Finite survival, local cycles, compatible densities, necessary gains, 和 unmatched port sequences each leave a full physical realization/closure obligation.

## 7. Concrete priorities

1. Supply one complete admissible T12 reference return, with exact J,C,U 和 a reproducible full transition check; otherwise complete a sound decision of the specified return language.
2. Alternatively, supply a concrete accepted original decimal certificate or a structurally valid return with both total gains nonnegative.
3. Preserve unresolved moving/growing-interior routes when applying bounded-centre or fixed-stream exclusions.
4. Repair #478 和 qualify the old graph claims in #479 before using them to prune search directions.
5. Reuse the existing positivity/admissibility/safety bridges; further wrappers do 不 fill the missing existential instance.

## 8. Verification boundary 和 required Lean gate

The publication pass inspected current primary sources, reconciled five synthesis reports, checked the active discussion for duplicate publication, reran the two small counterexamples, recomputed all eight centre-port primitive periods, 和 checked the paired p11 rotation. It did 不 run a full Lean build, `verify.py`, lean4checker replay, or the large graph searches. No new Lean theorem or verified decimal instance is claimed.

For any future Lean result, the owner's explicit requirements apply:

- No `sorry`, `admit`, custom `axiom`, or `native_decide`.
- Allowed axioms only: `propext`, `Classical.choice`, `Quot.sound`.
- No kernel-bypassing mechanisms: `set_option debug.*`, `run_cmd`, `run_elab`, `run_meta`, `addDecl`, `implemented_by`, `@[extern]`, `unsafe`, `elab`, or `#eval`.
- `verify.py` must replay every built module with `lean4checker`; retain actual endpoint axiom output 和 immutable source/build provenance.

Source reports consolidated: `lychrel-synthesis-audit.html`, `p196_synthesis_report.html`, `P196_Synthesis_Audit_2026-10-31.html`, `P196_synthesis_audit(2).html`, 和 `P196_Synthesis_Audit.html`. Their findings are published here with repository-accessible evidence rather than requiring access to private chats. No credit for a new decimal witness or exhaustive semantic verification of the whole corpus.
