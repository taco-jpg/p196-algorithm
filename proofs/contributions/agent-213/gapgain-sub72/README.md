# Agent #213 — sub-72 six-phase gap-gain split

Task: `agent213-gapgain-sub72-20261015`.

This contribution isolates a sharp consequence of the already accepted
six-phase accounting. For an accepted certificate with initial phase in
`{2,4,8,16,14,10}` and period (P<72), the existing endpoint gives:

- (18 \mid O), (18 \le O), and (2O \le P \le 4O);
- (P<72);
- each coordinate gain is nonnegative and divisible by 9;
- (O=2(D_g+D_h)).

Therefore (O<36), hence (O=18), and consequently
((D_g,D_h)) is exactly ((9,0)) or ((0,9)).

The Lean source packages this arithmetic consequence without introducing a
certificate instance, without changing the decimal orbit definition, and
without claiming existence of a qualifying return. Verification status is
WIP until compiled and axiom-audited under the repository's pinned
environment.

Relevant existing source:
- `Agent110.Checked.six_phase_constraints`
- `Agent110.Consequences.eighteen_overflows_gain_cases`

This is intended to narrow the next constructive search: every hypothetical
sub-72 six-phase return has one neutral gap and one gap gaining exactly nine.


## Independent verification

Fresh build with official Lean 4.19.0 against the archived dependency closure: `GapGainSub72.lean` exits 0; `six_phase_sub72_gain_split` and `six_phase_sub72_period_cases` depend only on propext, Classical.choice and Quot.sound. Status: LEAN-CHECKED.
