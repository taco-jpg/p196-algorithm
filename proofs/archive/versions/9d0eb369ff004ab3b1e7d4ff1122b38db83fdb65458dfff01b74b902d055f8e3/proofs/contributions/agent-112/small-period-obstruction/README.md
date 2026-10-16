# Agent #112: every checked return certificate has period at least eight

Status at initial source publication: all 13 new theorems compile with an axiom audit under official Lean4.19.0; the fresh nineteen-module closure rebuild is in progress. Independent review and integration are not claimed. Read the later evidence receipt rather than inferring success from a workflow launch.

## Exact endpoint

```lean
Agent112.SmallPeriod.checked_period_at_least_eight
  (cert : Agent109.Cert.Certificate)
  (hc : Agent109.Cert.check cert = true) : 8 <= cert.P
```

The original certificate format, checker and arithmetic semantics are unchanged. This applies to both phase classes, arbitrary finite exterior lengths and allowed trimming. No separate admissibility witness is assumed. It strengthens Agent110's check-only lower bound four; it neither supplies a certificate nor excludes every certificate.

## Proof and attribution

Agent110's cyclic phase equations give even phase coefficients. Their eight permitted even values split into the six-phase class2,4,8,16,14,10 and the two-phase class6,12. The six-phase class already has the stronger period bound42. The new two-phase code telescopes around the actual certificate links to prove an even period, so every checked certificate has even period.

Write O for the sum of terminal overflows. The existing checked accounting and carry budget imply positive even O and2O<=P<=4O. ForP=4, these force saturation2O=P. Agent4's existing saturation theorem, transported through Agent110's proved certificate projection and Agent112's automatic admissibility, gives8 dividingP, a contradiction. The new wrapper makes that saturation condition available without a six-phase premise.

ForP=6 in the two-phase class, all six charge equations modulo9 are instantiated from the actual LocalOK transitions. Eliminating the six exterior charges proves3 dividesO. Positive even O with2O<=6 forcesO=2, a contradiction. No divisibility premise is imposed on the initial exterior charge. The six-phase case is already impossible by42<=P. Combining these facts with the earlier lower bound four yields8<=P.

The generic arithmetic foundations, template semantics and checker are credited to their unchanged sources in SCOPE.json. This package does not count imported results as new work. All thirteen new theorem declarations carry explicit #print axioms commands; the proof roots depend only on propext, Classical.choice and Quot.sound.

## Reproduction and boundaries

```sh
python3 proofs/contributions/agent-112/small-period-obstruction/verify.py \
  --repo . --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /tmp/agent112-small-period-clean
```

The output directory must not exist. Add --expected-commit with the checked-out SHA for exact Git-head enforcement. SCOPE.json pins all nineteen modules by SHA256 and Git blob, and the verifier checks all module-owned safe declarations transitively, not just the final displayed theorem. It is the byte-identical author verifier from the sibling strip package, with attribution to Agent110's census method. A CI author replay is not an independent review.

The common-cut alternating-strip result lives in ../two-phase-obstruction and is not used as an unstated hypothesis here. Neither period8 nor period10 is excluded. Period>=12, complete two-phase exclusion, a accepted certificate, a positive Lychrel witness and the196 assertion remain unresolved by this package. Failed compiler attempts and their recovered exact sources are retained outside the accepted root.

Task: agent112-two-phase-certificate-obstruction; published continuation claim295c49811d351f9ead2d11d635c846945631d674. Agent1 retains main integration ownership.
