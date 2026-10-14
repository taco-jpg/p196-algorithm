# Fixed finite targets have bounded ancestry

This branch formalizes an unconditional decimal theorem. It does not prove
or disprove decimal Lychrel existence or 196's palindrome avoidance.

`FiniteAncestry.lean` imports the unchanged standalone
`continuation/LychrelDigitSums.lean`. It uses the existing checked
`DecimalWidthGrowth.numeric_width_bounds`,
`DecimalWidthGrowth.width_lower_bound`, and the ordinary decimal-length
representation lemmas. No growth hypothesis is postulated.

For positive `n`, the new numeric bridge proves

    r + 4*decimalLength(n) <= 4*decimalLength(T^r(n)) + 4,
    decimalLength(n) + floor(r/5) <= decimalLength(T^r(n)).

Consequently, if a positive integer `a` reaches a fixed target `N` after
`r` steps, then `r <= 4*decimalLength(N)`. The corresponding finite
admissible pair-word theorem gives `r <= 4*L` for a fixed target of width
`L`. Thus no positive-width target has an ancestor at any depth `r>=5L`;
the stronger exclusion is `r>4L`.

The file proves that ordinary numeric ancestry predicates descend with
depth and that their intersection over all depths is empty. It proves
the same descent and empty-intersection result for its numeric safe
ancestry definition. It also proves empty ordinary and safe ancestry
intersections for finite pair words, comparing the target's coefficient
function only on its actual finite width.

The safety convention matters. `HasSafeAncestor Safe N r` requires safety
at **every** time `k<=r`, including the ancestor and target. The pair-word
safe definition has the same convention. This is not equated with the
separate language recurrence `S_r=G(S_(r-1)\B)`: that recurrence tests
predecessors and can admit a target in `B`. Every member of that recurrence
still has an ordinary `r`-step ancestor, so the ordinary depth theorem
applies without identifying the safety definitions.

The root's ancestry conclusion is correct for canonical positive finite
words. It concerns a **fixed target** as backward depth tends to infinity.
An infinite forward orbit has changing targets `T^r(a)` of increasing
width; each may have depth-`r` ancestry without any fixed target having
arbitrarily deep ancestry. Therefore an empty backward intersection is
compatible with infinite forward orbits, including hypothetical Lychrel
orbits. Infinite-width digit objects are outside the theorem's domain.

Reproduce the complete source rebuild from the project root:

    python main_existence_attempt/ancestry_direct_pass/lean/check.py /workspace/scratch/fe6abe1df721/lean-runtime/lean

The executable above is the environment's Lean 4.19.0 wrapper. The raw
`lean-4.19.0-linux/bin/lean` executable needs the wrapper's loader shim.
The checker copies both sources to this directory's `build/`, compiles
the dependency and new module, checks source hashes stayed unchanged,
and audits every printed axiom list against standard Lean logical axioms.
`compile.log` retains compiler output. `verification.json` is written
only after both compilations and the audit succeed.

The principal new declarations are
`DecimalFiniteAncestry.numeric_width_five_floor`,
`numeric_ancestor_depth_le`, `numeric_no_ancestor_at_five_width`,
`numeric_ancestry_intersection_empty`,
`safe_ancestry_intersection_empty`, `pair_ancestor_depth_le`,
`pair_no_ancestor_at_five_width`, `pair_ancestry_intersection_empty`, and
`pair_safe_ancestry_intersection_empty`.

Fresh source rebuild: **PASS** with Lean 4.19.0. The unchanged dependency
compiled in 51.59 seconds and the new module in 0.77 seconds. All eleven
printed new declarations used only `propext` and `Quot.sound`.
Exact source hashes and successful exit codes are in `verification.json`.
No subprocess is left running, and existing source files were preserved.
