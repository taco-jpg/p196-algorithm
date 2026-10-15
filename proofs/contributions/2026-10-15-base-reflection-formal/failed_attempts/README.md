# Retained compiler failures

Attempt 1 used the unavailable unqualified name `pow_succ` and did not
normalize commuted integer products. Lean rejected `raw_high`.

Attempt 2 had the repaired raw identity, but the new residual identity's
simplifier did not distribute multiplication over subtraction in both
orientations or remove right multiplication by one. Lean rejected
`residual_high`.

The final source uses `Int.pow_succ`, explicit distributivity and
commutative normalization. These rejected drafts are retained as text;
they are not imported or counted as checked declarations.

Reset attempt 1 unfolded `qs` before its induction hypothesis could rewrite
the coefficient projection; the repair uses an explicit `change`.

Physical-width attempt 1 used reserved token `prefix` as an existential
variable, omitted simplification of `+0` in two recursion goals, and
unfolded `ordinaryTags` before a terminal-carry equality rewrite. Lean
rejected that draft. Its parser recovery warning is not an admitted proof
in the final sources; the complete fresh check rejects all disallowed
proof tokens and audits every final declaration.

The `*.replay.log` files are explicit reruns of these retained rejected
sources against the frozen prerequisite modules. They preserve compiler
failure evidence; none is included in the successful declaration count.

Seam attempt 1 referenced the coefficient name eliminated by a `rfl`
pattern. The repair uses the surviving name; the raw-injectivity proof
and hypotheses are unchanged.
