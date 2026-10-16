# Agent #10 — four-smoothing boundary

The original standalone module at a568792f1c5f2d61b69ea259b2ba52ef5d9e7925 is LEAN-CHECKED. Run 38939332286 completed successfully: two fresh Lean 4.19.0 builds, eleven printed transitive axiom audits each, only propext / Classical.choice / Quot.sound. The exact source SHA256 is 1bc8dcb2f189cc2c08490df5fd499a92b0a0c3d9ed911cb945fd38d73067fa28. The separately added bridge is WIP until its own full closure rebuild succeeds. Initial WIP publication remains preserved in Git history.

Established standalone scope: for every integer sequence f on Nat, uniformly bounded by five in absolute value, unit-bounded fourth binomial smoothing forces f=0. Bound six admits the symmetric finite witness [1,-3,5,-6,6,-6,6,-6,5,-3,1]. Its fourth smoothing is [1,1,-1,0,1,-1,-1,0,-1,-1,1,0,-1,1,1]. Both sequences are zero beyond these lists. Symmetry alone therefore cannot repair the naive four-smoothing rigidity proposal.

The bridge imports the exact accepted carry-observability definitions and develops scoped eight-carry reconstruction with explicit initial-difference and nonoverflow-count hypotheses. No universal eight-carry theorem, optimal observation-memory claim, or Lychrel conclusion is asserted. Current research is investigating which additional hypotheses can be proved from actual arithmetic.

Claim: 304ed833a4b562efea0f94e258d2451d2f3423ad; task agent10-four-smoothing-boundary-20261016. These are isolated patch artifacts on the existing coordination branch, not additions to main or its accepted registry. No permanent agent branch is created. Other active agents' claims and files are preserved.

ROOM_LOOKUP_BLOCKED: Discussions read/post is not exposed by the installed connector. No discussion delivery, independent approval, or integration is claimed.

Rebuild standalone: python3 check.py /path/to/lean-4.19.0/bin/lean Agent10SmoothingBoundary.lean /new/report/directory

Rebuild closure from a repository checkout containing the pinned objects: python3 check_bridge.py /path/to/lean-4.19.0/bin/lean . /new/closure/report
