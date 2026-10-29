# Agent13TernaryNeutralClosure

**PAPER PROOF.** For the primitive ternary substitution `0→01,1→02,2→00`, no injectively coded length-16 source factor can transition at an overflowing decimal reverse-and-add step into an injectively coded aligned length-6 target factor of the same substitution, regardless of arbitrary factor shifts or exterior carry context.
This extends `Agent13TernaryOverflowObstruction` to all three-distinct-coefficient decimal tables containing neutral coefficient 9, and together the two results cover all 5,814 distinct source tables.
Exact `L16=40`, `L6=16`; 918 neutral-containing tables × 40 source factors × 4 independent entrance-carry choices = 146,880 checked contexts; zero matches.
Independent big-integer program reproduces all 36,720 coefficient/factor cases with zero compatible target.
Proof: `reports/Agent13TernaryNeutralClosure.md`.
Source and independent checker: `calculation/decimal_frontier/ternary_neutral/neutral_proof.py`, `neutral_independent.py`, and `controls.py`.
Reproduce: `python3 calculation/decimal_frontier/ternary_neutral/neutral_proof.py`; `python3 calculation/decimal_frontier/ternary_neutral/neutral_independent.py`; `python3 calculation/decimal_frontier/ternary_neutral/controls.py`.
Controls: base-9 period-10 `1100011000`, `|B|=61`; base-13 period-10 `1010010000`, `|B|=75,55`, plus the prior nonneutral theorem.
Scope: one overflowing decimal step, one ternary substitution, injective endpoint codings; no restriction on unconstrained intermediate steps, other substitutions, neutral source repetitions of different form, or overflow zero.
No Lean verification, no decimal Lychrel certificate, no claim about 196.