# Additional execution evidence and historical limitations

All accepted Lean files are separate source files with printed dependency audits. The logs below preserve the additional successful phase refinement, capped exploration outcomes, and rejected development diagnostics. Historical failed compilations are NOT accepted proofs. In particular, `sorryAx` in a failed elaboration log is an error-state artifact and is absent from every accepted declaration's audit.

## AllPhaseRefinement.lean — successful compile, exit 0

Compiler: official Lean 4.19.0, commit 6caaee842e94. Source SHA-256: `97c48b0eaaeff5c058f664019d03c1484c8f992e78b756e51186acfe6bc93740`.

```text
'Agent8.returned_two_phase_mass_congruence' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.six_step_two_phase_forced_loss' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.no_repeatable_six_step_periodic_template_return' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.returned_six_phase_twelve_step_gains' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.returned_six_phase_eighteen_step_gains' depends on axioms: [propext, Classical.choice, Quot.sound]
```

## Capped exterior-only exploration — exact console outcome

Command: `python3 explore.py`. This starts only the 144 specified small exterior states. It is NOT exhaustive over all interfaces of width 200. All starts reached a cap and remain UNKNOWN beyond it. No cycle was found, and no global nonexistence conclusion follows.

```text
outer starts 144 nodes 31748 cycles 0 maxlen 200
outer results Counter({"('cap', 14, 201)": 30, "('cap', 2, 201)": 27, "('cap', 6, 201)": 20, "('cap', 16, 201)": 17, "('cap', 12, 201)": 16, "('cap', 4, 201)": 15, "('cap', 10, 201)": 15, "('cap', 8, 201)": 4})
```

## Necessary exterior graph — exact console outcome

Command: `python3 exterior_graph.py`. Potential lists include an unused p=0 entry. Closed-walk overflow counts concern the necessary scalar graph, not global realizability by arbitrary whole-word paths.

```text
upper [0, 0, 0, 0, 1, 0, 1, 1, 1, 2, 1, 1, 1, 2, 1, 2, 2, 2, 3]
lower [0, 4, 3, 2, 2, 2, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
1 []
2 [1]
3 [1]
4 [1, 2]
5 [2]
6 [2, 3]
7 [2, 3]
8 [2, 3, 4]
9 [3, 4]
10 [3, 4, 5]
11 [3, 4, 5]
12 [3, 4, 5, 6]
```

The period-three line is `3 [1]`. The first publication of this evidence page transcribed that one line incorrectly as `3 [1, 2]` and immediately flagged it; this revision restores the exact retained output. No period-three two-overflow claim is made, and no Lean source or theorem was affected.

## Rejected first PeriodObstructions development compile

The initial transient source was edited during development and was not separately snapshotted. The original compiler diagnostics below were retained, but they are not a standalone reproducible source package. The published accepted source fixes these issues and has a fresh successful audit.

```text
PeriodObstructions.lean:104:14: error: unsolved goals
case succ
a : Word
m n : Nat
ih : orbit a (m + n) = orbit (orbit a m) n
⊢ stepWord (orbit a (m.add n)) = stepWord (orbit (orbit a m) n)
PeriodObstructions.lean:173:22: error: unknown constant 'Nat.cast_add'
PeriodObstructions.lean:173:36: error: unknown constant 'Nat.cast_one'
PeriodObstructions.lean:221:2: error: omega could not prove the goal:
a possible counterexample may satisfy the constraints
  a ≥ 0
  a + 9*b ≥ 2
  2 ≤ 2*a + 9*b ≤ 3
where
 a := dh
 b := (dg - dh) / 9
PeriodObstructions.lean:227:2: error: omega could not prove the goal:
a possible counterexample may satisfy the constraints
  a ≥ 0
  0 ≤ a + 9*b ≤ 1
  3 ≤ 2*a + 9*b ≤ 4
where
 a := dh
 b := (dg - dh) / 9
'Agent8.mass_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.normalize_mass_mod' depends on axioms: [propext, Quot.sound]
'Agent8.step_mass_mod' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.six_multiple_mass_mod' depends on axioms: [propext, sorryAx, Classical.choice, Quot.sound]
'Agent8.finite_exterior_certificate' does not depend on any axioms
'Agent8.closed_path_bounds' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.returned_period_at_least_four' depends on axioms: [propext, Quot.sound]
'Agent8.six_step_forced_loss' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.no_repeatable_six_step_return' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.short_return_equal_gains' depends on axioms: [propext, Classical.choice, Quot.sound]
'Agent8.twelve_step_gains' depends on axioms: [sorryAx]
'Agent8.eighteen_step_gains' depends on axioms: [sorryAx]
```

The fixes were ordinary explicit proof steps: congruence for the orbit recursion, supported integer cast lemmas, and invoking the proved equal-gains lemma before the period-12/18 arithmetic. None introduced an additional axiom or accepted a failed goal.

## Rejected mathematical shortcut

The saturated leading cycles cannot be fed directly to the repository's full-high-region theorem. That theorem assumes every coefficient is in 9 through18, while the proposed shortcut knew only the exterior. The missing hypothesis was not established, so no such inference was used or published as a theorem.
