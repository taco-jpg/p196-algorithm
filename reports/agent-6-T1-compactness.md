# Agent 6 — T1 fixed-period prefix-graph compactness criterion

**PAPER PROOF (conditional only).** This is a mathematical limitation of the existing *necessary projection*, not an actual base-10 certificate or an unconditional decimal impossibility theorem. Coordination: #289, follow-up to finite-prefix experiments. No Lean theorem is claimed.

## Graphs and projection

For base 10 and a center-length cap D, let G_R be the finite graph of admissible symmetric centers C, entering carry e with outgoing carry 1-e, and the first R coefficient entries of exterior B padded by an infinite neutral-9 suffix. The exterior transition allows both possible inward high carry bits at position R; all R output entries are calculated by the exact digit arithmetic, while all symmetric center 9-pair trims are allowed. Exterior and center must emit the **same** overflow g, although incoming center e is not required to be recovered from the full, unknown B. Thus G_R is a safe **overapproximation** of genuine A120 checker states.

**Lemma 1 (PAPER).** Truncating the final exterior coefficient gives a graph homomorphism q_R:G_(R+1) → G_R preserving center, e, overflow g and legality of edges. For a length R+1 transition with high carry h_(R+1), the carry into its position R equals floor((a_R+h_(R+1))/10), one of the two allowed high bits in G_R. Lower-digit forward and reverse normalizations therefore agree with the R-prefix calculation. Center equations remain identical.

## Fixed-period compactness

Let W_R(p) be the finite set of **phase-indexed closed walks of p edges** in G_R (primitive period may divide p), for any fixed p>=1. The truncation maps W_(R+1)(p) into W_R(p).

**Theorem 2 (PAPER).** If W_R(p) is nonempty **for every R**, there exists a compatible tower (w_R) with q_R(w_(R+1))=w_R for all R. Proof: form the rooted tree of finite p-walks at every depth, with edges given by truncation. Every level is nonempty, and the tree is finitely branching because alphabets, period and center cap are finite. König's infinity lemma supplies an infinite branch. Consistent finite carry witnesses can be retained by the same finite-branching diagonal argument.

Such a tower defines a **formal infinite exterior coefficient configuration** satisfying every finite local projected equation and the periodic center equations. Critically, **it need not have an eventually neutral-9 tail, need not obey the genuine finite-B terminal carry and center/exterior coupling, and need not define any finite integer**. It is *not* a `cycleOK 10` certificate, cannot prove decimal Lychrel existence, and cannot refute existence.

Contrapositive: if no formal infinite p-periodic projected solution exists, some finite R already has W_R(p)=empty. That is an existential finite obstruction for fixed p, **not** an effective uniform R bound. Likewise finite observed cycles through R=13 (Agent6's separately scoped audit) do not imply W_R(p) remains nonempty at every larger R, especially as periods may change.

## Independent arithmetic sanity test

Run `python3 calculation/agent-6/check_projection_compatibility.py`, standard library only. 100,000 seeded source coefficient words (lengths 2..15), both inward high bits, zero mismatches under R+1→R truncation. Observed: `PREFIX_PROJECTION_HOMOMORPHISM PASS 100000 random source words; no counterexample`. The test is COMPUTED and is not the proof of the lemmas.

## Provenance and scope

Credits: Agent4's first-column carry recurrence, Agent101 and Agent6's earlier prefix × center necessary graphs (PRs #332, #345), and the independent real p24 center-loop work. This report concerns only projected *formal* objects and deliberately does not compete with Agent117/101/106's work on genuine finite exterior cycles. No `RESULTS.md`, `README.md`, or Lean changes. `tools/verify.py --changed` has not been run in a full checkout; this code/report-only PR must remain **UNVERIFIED / DO NOT MERGE** pending review.
