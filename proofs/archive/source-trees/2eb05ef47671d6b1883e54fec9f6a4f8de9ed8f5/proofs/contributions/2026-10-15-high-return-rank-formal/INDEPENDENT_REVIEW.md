# Independent review of the finite high-return rank certificate

**Verdict: PASS.** Independent gate-review stream, 2026-10-15. I read the complete accepted Lean source, generator, README, generation report, verification report and compile log, and independently compared the complete data with the separately constructed actual-bridge graph. No additional Lean compilation was needed or performed.

The reviewed Lean source has SHA-256 `76ce0aefdcf8ed6bea047c5d8b718d23ab02bfaf18bfb96211f8fa13269218d8`. Exact hashes for the reviewed generator, reports, data and log are retained in `independent_source_audit.json`.

For indices below 900 the decoding gives exactly `A in 10..18` and `B,C in 9..18`. All input natural-number subtractions are justified on this domain: `A>=10`, `A+B>=19`, and `B+C>=18`. The accepted-output guard likewise ensures that `U-10`, `V-9`, and the final subtraction of nine in the target index cannot underflow. That final expression equals `100*(U-10)+10*(V-9)+(W-9)` under its guard. The finite check additionally verifies every accepted target is below 900.

The transition arithmetic agrees exactly with the independent written bridge: it computes the first high-carry prefix `(a,x,y)`, the low incoming carry `x/10`, the two successive high-side incoming carries, the actual no-overflow test, and the sum of the two output digits at each reflected position. The parameter `w` is restricted to zero or one by each theorem using an edge. The function's behavior outside the finite index/control range is not used.

The independent audit compares all 1,800 controls, including every rejected control, with `../2026-10-15-full-high-return/prefix_certificate.json.gz`. All 258 admitted targets and all 900 ranks agree. It separately parses the actual balanced rank expression from the Lean source and evaluates every one of its 900 in-range values, rather than trusting the generator's rank array. Replaying the generator in an isolated temporary directory reproduces the accepted Lean source, generation report and compressed finite data byte for byte. The frozen package is unchanged.

`finite_check` is proved by ordinary kernel-checked `decide`, not `native_decide`. Its assertion checks both the rank bound and strict decrease with target closure for both controls at every input index. `checked_vertex`, `rank_le_three`, and `edge_decreases` correctly extract those exhaustive checks. `no_four_edges` repeatedly obtains the next index bound before applying the next edge theorem; four strict decreases contradict the initial natural-number rank bound of three. No endpoint or fifth vertex is left outside the checked domain.

The successful verification report matches the current source hash and the complete compile log. Its finite evaluation theorem has no axioms; the other four declarations use only `propext` and `Quot.sound`. The source contains no proof placeholders or additional axiom declarations. The retained initial failed attempt used the wrong Boolean lemma name; the accepted source uses `Bool.and_eq_true_iff` and all five final declarations are covered by the successful report.

The scope is accurate: this is a kernel certificate excluding four edges in a specific finite arithmetic graph. The connection from actual reverse-and-add returns to that graph, the neutral-exterior overflow exclusion, and the small-width cases remain the separate written mathematical proof. The package does not present those obligations as already formalized and does not establish a standalone formal theorem about the orbit of 196.

Reproduce this source/data review from the repository root:

```sh
python proofs/contributions/2026-10-15-high-return-rank-formal/independent_source_audit.py
```
