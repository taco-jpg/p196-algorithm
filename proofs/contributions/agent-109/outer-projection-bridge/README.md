# Agent #109 — Lean bridge for Agent #7's complementary exterior map

Task record: `proofs/coordination/tasks/agent109-outer-projection-bridge.json`.

**Status: LEAN-CHECKED (local fresh build, Lean 4.19.0 `6caaee842e94`). Not
independently reviewed. No cycle, safe orbit or statement about 196.**

Agent #7's `OuterBounds.lean` (branch `agent7/outer-boundary-audit` @ `da4a179`)
kernel-checks finite facts about the exterior map
`P196.Agent7.Finite.outerNext` and notes: *"The actual whole-word-to-outer
projection remains a separate written bridge."* The cap-5/6/7 exterior
computations of Agents #101/#102 use the same map. This package supplies that
bridge in Lean.

## Proved

* `Agent109.Outer.outerNext_eq`: for every interface `A` and center `C`,
  `outerNext ⟨c,B⟩ = ⟨2t_c, stripSuffix (2t_c) (Br c B A C)⟩` — Agent #7's raw
  exterior word is exactly the returned exterior block `B_r` of identity (8)
  (`Agent109.stepWord_template`), maximally stripped of trailing phase letters.
* `stripSuffix_spec`, `succ_bounded`: stripping only removes `c'` letters; the
  successor blocks `B_r, A_r, C_r` have coefficients ≤ 18.
* `actual_step_outer`: if `pairWord n = template c B A C (g+2) (h+2)` then
  `pairWord (step n)` is a template with phase/exterior `outerNext ⟨c,B⟩`,
  interface `A_r`, center `C_r`, first band `≥ g` and second band `h+γ`.
* `actual_outer_orbit`: while `2i ≤ g` and `2i ≤ h`, the ordinary orbit at time
  `i` has a template representation whose phase and trimmed exterior are the
  `i`-th iterate of `outerNext`.
* `actual_cap2_exit` (+ `Agent109.OuterCompat.lychrel_cap2_exit` for
  `Lychrel196.orbit`/`Agent8.template`): if `n` realizes a template with phase
  `2(p+1)`, bounded blocks, exterior of length ≤ 2 accepted by Agent #7's
  `validOuter`, and both bands ≥ 14, then for some `i ≤ 7` the actual orbit
  integer at time `i` has a template representation whose exterior is Agent #7's
  `outerIterate i` state and has length > 2. This composes Agent #7's
  kernel-checked `cap2_exits_by_seven` (no axioms) with the bridge.

Axioms: only `propext`, `Classical.choice`, `Quot.sound` (see `build_log.txt`).

## Scope

The cap-two exit is about the maximally trimmed exterior coordinate of a
template representation; it does not say the integer leaves every possible
template family, and it is no termination or palindrome result. Larger caps
remain the computational results of Agents #101/#102 (outside Lean here).
`agent7-deps/` holds unmodified copies of Agent #7's two modules with their
pinned commit and hashes (`build.sh` checks them).
