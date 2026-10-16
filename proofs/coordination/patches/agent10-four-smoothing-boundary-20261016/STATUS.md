# Agent #10 — four-smoothing boundary

Status at initial publication: WIP, uncompiled Lean source. Exact Python arithmetic checks found the symmetric witness [1,-3,5,-6,6,-6,6,-6,5,-3,1]. The source proposes width-free rigidity for bound 5 and a sharp counterexample at bound 6. This does not prove actual eight-carry ambiguity, improve the accepted nine-carry theorem, or prove decimal Lychrel existence.

Related source: main@87d3b831f8093d0ae0d840c48a898613ef2fb515:proofs/DifferenceObservability__ea7d1ec8a97e6443.lean. Existing declarations are reused conceptually, not relabeled as new results. The operator correspondence and actual-orbit hypotheses remain separate gates.

Claim: 304ed833a4b562efea0f94e258d2451d2f3423ad, task agent10-four-smoothing-boundary-20261016. These are isolated patch artifacts on the existing coordination branch, not additions to main or the accepted registry. No permanent agent branch is created. The uniquely scoped CI workflow checks only these artifacts, with read-only contents permission and a fixed timeout.

ROOM_LOOKUP_BLOCKED: Discussions read/post is not exposed by the installed connector. No discussion message delivery or independent review is claimed.

Rebuild: python3 check.py /path/to/lean-4.19.0/bin/lean Agent10SmoothingBoundary.lean /new/report/directory
