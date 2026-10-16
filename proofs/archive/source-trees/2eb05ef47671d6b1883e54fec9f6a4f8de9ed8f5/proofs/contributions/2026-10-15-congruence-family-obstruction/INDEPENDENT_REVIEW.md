# Independent review of the congruence-preserving paths

**Verdict: PASS.** Independent gate-review stream, 2026-10-15. I read the complete note and producer, checked the all-parameter arguments, and independently verified the retained path archive using arithmetic radix division and ordinary integer reversal. The reviewed file hashes and exact finite counts are recorded in `independent_audit.json`.

The scope is correctly pathwise. For each selected family parameter and finite delay, the construction supplies one terminating finite path. It does not provide a single function on all integers, preserve an arbitrary genuine trajectory prefix, or establish the stronger complete pair-word quotient property of the cited external countermap. The first edge and final edge are genuine reverse-and-add transitions; the remaining edges preserve only the explicitly stated properties. This distinction is present in the theorem statement, proof, checker and report.

For `k=floor(7R/4)+1`, the first genuine output from `2(10^k-1)` is exactly `11(10^k-1)`, divisible by 99. Its stated digit word, width and digit sum are correct for `k>=2`. After that point the modulo-nine and parity-sensitive modulo-eleven laws hold on any edge between multiples of 99, so the construction really does preserve both laws without imposing the true update.

The tails in the artificial chain have the required residues: `10^e` is congruent to ten or one modulo 99, while the two selected tails cancel those values. The labels `990a` contribute zero. The terminal predecessor has the same divisibility. The bound `990a+989<10^(a-1)` holds at `a=5` and is preserved by increasing `a`: the additive increase 990 is less than nine times the preceding positive left-hand side. Hence the leading and trailing digits do not overlap. Chain nodes have exterior sum ten and are outside both exact immediate-palindrome predecessor classes. The terminal predecessor's three-digit tail is separated from its reflection because its exponent is at least six; every pair coefficient is at most nine, so its true next output is a palindrome.

The entry, chain and exit inequalities give strict growth, output below eleven times the source, and width increase at most one. Intermediate artificial edges increase width by one. The genuine terminal edge has no overflow. These facts imply the stated lower bound on width at each time, including the explicitly handled `R=0` and `R=1` cases. All preceding vertices have unequal endpoint digits, and the exact first positive hit times are therefore `ell+4`, or `ell+5` for the small exceptional construction. There is no inference from arbitrary finite survival to one infinite actual orbit.

The quantitative carry-budget obstruction also holds for **every** `R>=3`, not just the stored controls. A genuine transition from `y_k` has source digit sum `9k` and width `a=k+2`; at most `a` outgoing binary carries give the lower target digit-sum bound `9a-36`. At `R=3`, `a=8` and the constructed target is `100008909`, of digit sum 27 rather than the required minimum 36. For all `a>=9`, the bound `990a+989<10^(a-5)` starts with `9899<10000` and has the same valid induction step. The target then has digit sum at most `1+9(a-5)=9a-44`, strictly below `9a-36`. Since `R>=4` gives `a>=10`, these two cases cover every claimed parameter. Thus this specific congruence-preserving construction fails a stronger necessary actual-transition condition. The note does not claim that every conceivable construction preserving that condition must fail.

The independent archive verifier checks all 134 exact cases, including their formulas, 8,259 stored states and 8,125 edges. It checks genuine endpoint transitions, every edge's congruences, numeric and width bounds, the actual one-step palindrome predicate, first-hit indices, and all 128 retained carry-budget violations. It also checks the compressed and recovered byte counts and hashes against the producer report. It neither imports nor reruns the producer and leaves its files unchanged.

Reproduce the independent finite audit from the repository root:

```sh
python proofs/contributions/2026-10-15-congruence-family-obstruction/independent_audit.py
```

This is a written mathematical review plus finite arithmetic verification. It adds no Lean theorem and asserts no complete-termination model with all actual arithmetic invariants, no persistent safe family, and no decimal Lychrel witness.
