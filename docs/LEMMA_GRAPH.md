# Proof dependency graph: all-time certificates and decimal target T*

**Route:** agent-Q37, CROSS-POLLINATION 7  
**Status:** UNDECIDED for base 10. This file is a dependency/reduction map, not a decimal existence claim.

## Exact open goal

For decimal reverse-and-add, let step(n) = n + reverse10(n), orbit(n,0) = n, orbit(n,t+1) = step(orbit(n,t)), and Pal(n) mean that the canonical decimal digits are palindromic. The goal is:

[
\exists n\in\mathbb N\;\forall t\in\mathbb N,\quad \neg Pal(orbit(n,t)).
]

The current T* target is the rooted phase-0 p12/m9 template. Let B have 34 coefficients, W have 9 coefficients, and U be one of the 30 charge-zero length-3 rotations of (9,a,18-a), for even a from 0 through 18. For a finite junction J and palindromic coefficient centre C, put

[
H(q,k)=B\mathbin{++}W^q\mathbin{++}J\mathbin{++}U^k,
\qquad P(q,k;J,U,C)=H(q,k)\mathbin{++}C\mathbin{++}\operatorname{reverse}(H(q,k)).
]

All coefficient words must have a canonical positive decimal source realization; in particular, an odd-length centre must have an even middle coefficient. The rooted overflow word is (100010001000) repeated ten times over the 120-step macro, with exactly 30 genuine overflows.

## Dependency graph

Arrows mean “is used by”; dashed edges are conditional or not yet instantiated.

```mermaid
flowchart TD
  S[Decimal semantics: reverse10, step, orbit, Palindrome, IsLychrel] --> I[Generic all-time induction: Lychrel196.lychrel_of_invariant]
  S --> C0[Canonical digits and exact pairword arithmetic]
  C0 --> C1[Neutral one-band edge soundness]
  C1 --> C2[Agent120.Neutral.lychrel_of_cycle]
  C0 --> A1[Absorbing-band exact step]
  A1 --> A2[AbsorbingBand.lychrel_of_lcycle]
  C0 --> L1[Lattice exact step and reflection]
  L1 --> L2[LatticeBand.lychrel_of_lcycle]
  C2 --> EX[Concrete Lean-checked certificate instances]
  A2 --> EX
  L2 --> EX
  EX --> CTRL[Base 9 and base 13 controls; not base 10]

  C0 --> R[Missing T*: canonical physical 120-step return at q=14,k=100]
  T12[T12Rooted120CutPumping: fixed J,U,C return at reference width iff all q>=14,k>=100] --> W[Uniform macro return P(q,k) to P(q,k+5)]
  R --> W
  ROOT[Reported pi175 root-only guard: every 120-state block is nonpalindromic when the pairword begins with B] --> SAFE[All-time nonpalindrome for the rooted orbit]
  W --> SAFE
  I -. all-time logical endpoint .-> SAFE
  SAFE --> GOAL[Decimal Lychrel witness]

  RED[pi185 finite-product reduction: 120-layer two-ended carry NFA] -. decides existence of .-> R
  PHY[Complete physical transition relation: both carry ports, gamma-one lag digit, midpoint and canonical source] -. required to instantiate .-> RED
  G[pi179 bounded-cycle theorem, conditional on a finite graph of genuine physical edges] -. only after .-> PHY
```

## Existing all-time proof nodes

| Node | Exact scope and source | Dependency/use |
|---|---|---|
| Decimal semantics and general induction | LEAN-VERIFIED: [LychrelDigitSums.lean](../lean/P196/Foundations/LychrelDigitSums.lean), including Lychrel196.reverse10, step, orbit, Palindrome, IsLychrel, DecimalLychrelExistence (an open proposition), and lychrel_of_invariant. | Supplies the meaning of the goal and a generic induction principle. It does not supply an invariant or witness for base 10. |
| Neutral one-band certificate | LEAN-VERIFIED: [A120Base.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Base.lean), [A120Template.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean), [A120Certificate.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Certificate.lean). Main endpoints include step_eq_val_pairs, step_tmpl, not_isPal_tmpl, edge_step, chain_run, lychrel_of_cycle and lychrel_of_entry. | A closed nonempty edge cycle, exact guards, and nonnegative accumulated gap drift imply all-time survival. This one-band checker is not itself a checker for T*'s two bands and junction. |
| Absorbing-band certificate | LEAN-VERIFIED: [AbsorbingBand/Step.lean](../lean/P196/AbsorbingBand/Step.lean) and [AbsorbingBand/Cert.lean](../lean/P196/AbsorbingBand/Cert.lean); concrete instance [Base13.lean](../lean/P196/AbsorbingBand/Base13.lean). | Exact all-length step and cycle induction; base 13 is a control, not a decimal instance. |
| Lattice-band certificate | LEAN-VERIFIED: [LatticeBand/Band.lean](../lean/P196/LatticeBand/Band.lean), [Digits.lean](../lean/P196/LatticeBand/Digits.lean), [Pairs.lean](../lean/P196/LatticeBand/Pairs.lean), [Step.lean](../lean/P196/LatticeBand/Step.lean), [Cert.lean](../lean/P196/LatticeBand/Cert.lean); concrete [Base9.lean](../lean/P196/LatticeBand/Base9.lean). | Exact periodic-band step, nonpalindrome guard, and cycle induction; base 9 is a control, not a decimal instance. |
| T12 insertion/pumping | PAPER PROOF as scoped in [T12Rooted120CutPumping.md](../results/T12Rooted120CutPumping.md), with reproducible checks in [cut.py](../calculation/new_structures/T12/cut.py). For fixed J,U,C, Return(q,k) is equivalent to Return(14,100) for every q≥14,k≥100; the exact target is P(q,k) to P(q,k+5) in 120 genuine decimal steps. | Converts one reference-width physical return into a uniform family. It does not find that return. The independent J,C search remains unresolved. |
| Root-only 120-state safety | PAPER PROOF as reported in the “Issue #475 migration and new proof-relevant reductions” section of [FOCUS_SWARM.md](FOCUS_SWARM.md): a canonical positive source of length at least 68 whose symmetric pairword begins with the rooted 34-coefficient B has no palindrome at states t=0,...,119. This is not labelled LEAN-VERIFIED here. | Once the 120-step return is available, the same rooted prefix is restored at each macro boundary, so this guard covers every ordinary step. |
| Conditional regular-language safety | PAPER PROOF, conditional: [AgentN07FoldedRegularSafety.md](../results/AgentN07FoldedRegularSafety.md). The accepted language must be nonempty, physically realizable, forward-closed under the exact two-sided carry transducer, and palindrome-safe. | A different all-time route. No decimal invariant language with an actual seed is supplied. |
| Decimal insertion commutation outside T* | PAPER PROOF, scoped: [AgentN10UniversalPumpLemma.md](../results/AgentN10UniversalPumpLemma.md). | Exact insertion commutation for the p8/m20 exterior does not establish T*'s p12/m9 physical return. |
| Phase/length necessary conditions | PAPER PROOF: [CERT_SPEC_Q01.md](CERT_SPEC_Q01.md). For a fixed literal paired template with period p, overflow sum S, and band period m, a literal return after k steps with gain g requires k=p r and rS=2mg; additional coefficient-mass congruences apply. | Necessary arithmetic filter only. For T*, 120 steps and 30 overflows match the required gain of five U3 copies: 30=2·3·5. This agreement is not a physical seam return. |

## The exact missing node

Name: **PHYSICAL_TSTAR_RETURN_AT_REFERENCE_WIDTH**.

Find one U, finite J, and palindromic coefficient centre C such that the canonical positive source with pairword P(14,100;J,U,C) has an exact 120-step ordinary decimal trajectory whose terminal pairword is P(14,105;J,U,C), with every intermediate phase and both physical carry ports checked. The midpoint/source-realizability conditions and all 30 overflow positions must be exact, not inferred from a bulk SCC or a pairword-only projection.

The recorded pi185 reduction proposes a finite decision procedure: construct the 120-track padded synchronous product of the exact two-ended carry NFA with the fixed U^5 insertion, then decide nonemptiness for all 30 U rotations. Its stated 82 reachable nonterminal states, 1,556 symbol arcs and lag bound of 120 are a proposed construction target; the full product has **not** been built or decided. Treat these figures as a reduction report, not a completed computation or verified theorem.

If a canonical witness is found, T12 insertion lifts it to all q≥14,k≥100. At macro boundaries k becomes 100+5r, so the rooted prefix is restored and the reported root-only guard excludes palindromes in each 120-step block. That composition would prove an all-time decimal witness, subject to checking the stated guard proof and the full physical return. If the product is empty, the conclusion is limited to this fixed-J/C, phase-0 T* family; moving seams, phase-changing centres and other template formats remain open.

The pi179 bounded-cycle result is conditional on an already complete finite graph whose edges are genuine physical transitions. It cannot be used to fill in missing carry ports or to declare the pi185 product complete.

## Status discipline

- LEAN-VERIFIED means the endpoint theorem and its actual instance are kernel-checked.
- PAPER PROOF means the all-quantifier mathematical argument is written and its hypotheses are explicit.
- COMPUTED means a stated finite computation was actually completed with a reproducible command and independent controls.
- UNDECIDED means no such result has been established.

No base-10 all-time certificate is known from the nodes above. This graph intentionally marks the missing physical return rather than converting necessary congruences, finite-width replays, or conditional graph bounds into an existence claim.
