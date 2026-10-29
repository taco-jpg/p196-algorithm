# Agent13TernaryP8Rotation

**PAPER PROOF.** For the primitive ternary substitution `0→01,1→02,2→00`, a length-32 interior factor injectively encoded by distinct decimal pair coefficients cannot return after overflow `01010101` to an aligned injectively encoded length-28 factor, at any source/target shifts, even with seven unrestricted intermediate pairwords.
Exact two-sided nondeterministic carry transducer allows all four entering-carry combinations per step; an eight-step prefix-cropping lemma reduces the longer exclusion to a complete finite census plus exceptional cases.
**COMPUTED sublemma:** all 5,814 coefficient tables ×72 length-28 source factors = 418,608 cases, cap 50,000, zero capped, maximum 1,260 states. Exactly 18 tables admit four short-window necessary matches each (72 total); all other 5,796 tables excluded.
Independent Python checked all 18 exceptional tables on all 80 length-32 factors (1,440 longer cases), with zero aligned length-28 endpoint matches, and reproduced each shorter count.
Controls: 3,000 ordinary integer steps, 5,000 prefix checks, exact factor-language equality, mandatory b9 `1100011000` / B61 and b13 `1010010000` / B75,B55.
Proof: `reports/Agent13TernaryP8Rotation.md`.
Complete sources, compact data, independent checker and runner: `calculation/decimal_frontier/ternary_p8_rotation/`.
Reproduce from repository root: `sh calculation/decimal_frontier/ternary_p8_rotation/run.sh /tmp/agent13-ternary-p8-rotation`.
Scope: only the given substitution, overflow `01010101`, injective endpoint codings and interior length≥32 aligned transition; not other centres, shorter windows, or the base-10 Lychrel question.
No Lean verification is claimed.
