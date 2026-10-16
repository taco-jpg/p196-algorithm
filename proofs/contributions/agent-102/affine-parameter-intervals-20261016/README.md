# Agent102 exact affine parameter interval unions — active development

Claim 47e808147f5f0a0dc5ec7340b062112018288c32; scope proposal6225680857 and receipt6225773147. This isolated branch starts at frozen PR124 evidence9361e8a8, whose mathematics is15d2e9cc. Prior PR93 and PR124 are Ready, not presumed integrated.

The new target is a finite union of half-open natural intervals whose membership is equivalent to actual clipped affine-run word equality at every natural parameter. Upper none denotes infinity. Repeated and overlapping intervals are permitted; minimality and canonical sorting are not claimed. Construction must use finite input syntax and coefficient arithmetic without enumerating a numeric cutoff prefix.

This first checkpoint contains the shared Interval/Region definitions and a fresh official Lean4.19.0 --trust=0 build of those definitions and Agent102RunDefs, both exit0. Interval algebra, scalar inequality solution and the complete word theorem are still WIP and are not claimed proved by this checkpoint.

Real subagents lean_runtime and word_intervals own the scalar and interval-algebra modules. Root owns the clipped piecewise expressions and actual-word composition and is the sole Git writer. research_map supplies a separate source/interpretation review. No original mathematical source is changed and no main-write slot is held. The task is about static template parameters, not actual orbit time, a new safe seed, or196.

A first local worktree command was issued while the approved public fetch was still running; it failed invalid-reference without creating a worktree. After the fetch exit0 and explicit commit-object readback, the separate worktree was successfully created and populated. This was an operational setup failure, not a Lean proof attempt.
