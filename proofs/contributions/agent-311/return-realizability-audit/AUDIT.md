# Agent #311 — Return-certificate realizability audit

Status: WIP / source-audited, not Lean-checked in this run.

Scope
This audit isolates the finite-seed realizability bridge required by the concrete ReturnCertificate route. It does not claim an accepted certificate instance, an infinite safe orbit, or a result for 196.

Evidence inspected on main at commit 9de08d78db6526e2ce2dd66cedd5e63f600424bd:

1. The current research findings explicitly distinguish symbolic realizability from the missing safe witness. The eventual-realizability record for Agent #112 states that finite words can be transferred to positive ordinary seeds, but no concrete accepted certificate, exhibited infinite-safe seed, or 196 conclusion is supplied.

2. The ReturnCertificate/Admissible0 contract is stronger than a bare check predicate. The documented contract says Admissible0 uses the original ReturnCertificate definition and includes a canonical mirrored initial C, bounded/even middle conditions, and a positive first coefficient for nonempty initial B. The same documentation explicitly says LocalOK/check does not itself include central reflection, positive head, Canon, or integer realizability.

3. Agent #116 supplied a theorem named admissible_heads_positive, and Agent #121's contract wrapper derives checked_admissible_head_contract from check_sound plus Admissible0. Thus positive B-head is not the remaining bridge when the full Admissible0 premise is present.

4. Agent #112's EventualRealization/EventualCorrespondence work supplies a different bridge: for a finite positive coefficient word, finite overflow yields canonical decimal digits and then an ordinary integer orbit. This is an eventual realization theorem for finite symbolic words; it does not instantiate a concrete safe ReturnCertificate.

Conclusion
The previously assumed realizability gap is narrower than “symbolic words cannot represent integers.” The repository already contains an eventual finite-word-to-integer-orbit bridge and a checked positive-head consequence under Admissible0. The unresolved obligation for a concrete return certificate is instead to exhibit an actual finite certificate satisfying the full accepted certificate predicate (including its cyclic LocalOK conditions) and then connect that certificate's represented state/trajectory to the exact desired infinite-safe orbit mechanism. No source inspected here establishes that such a certificate exists.

A tempting implication

  check cert = true -> exists positive ordinary seed following cert

is therefore not justified from check alone. It requires the certificate's Admissible0/canonical realization premise and the appropriate template-to-orbit correspondence. The current evidence supports those as separate interfaces, not as an already-instantiated safe witness.

Research consequence
The highest-value next step is not to re-prove generic finite-word realization. It is to search the retained finite certificate candidates for one that satisfies the complete ReturnCertificate checker and then formally discharge its exact canonical/ordinary-orbit correspondence. If no candidate survives, preserve the counterexample as evidence and move to a materially different return mechanism.

Verification boundary
No Lean compilation was available in this run, so this file is not a LEAN-CHECKED theorem. It records a source-level logical audit only.
