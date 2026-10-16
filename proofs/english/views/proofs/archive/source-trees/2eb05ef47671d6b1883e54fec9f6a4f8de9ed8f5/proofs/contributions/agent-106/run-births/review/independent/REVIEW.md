# Agent 106 independent mathematical and Lean review

Reviewer: an independent reviewer, not an author of the three reviewed modules. This report covers only `NoOverflowBirths.lean`, `BirthFamily.lean`, and `OverflowBirths.lean`; it does not replace separate reviews of BaseBirths or PopulationObstructions. Author source was not modified, and no Git writes were executed.

## Review conclusion and exact scope

Independent mathematical/interface review and a complete Lean rebuild all passed, with no required corrections found. `build-001/verification.json` has final status `PASS`: the foundation, three target modules, and AllAxioms actually executed with exit 0. Axiom audits passed for all 56 public declarations (51 theorem, 5 def). `source_inventory.json` records complete SHA-256 hashes and declaration counts for the reviewed version.

The acceptable conclusions are:

- For any actual `Admissible L q`, when the actual terminal carry is 0, the iff conditions for 0/18 output and fresh births hold at physical columns `i < L`; the center excludes the old-9 branch.
- When the actual terminal carry is 1, all interior columns `0 < i < L` satisfy the 0/18 output conditions, the fresh-birth conditions excluding old adjacent pairs already equal to the same extreme, and the necessary adjacency to 9. Exact values and nonextremality of the two new endpoints `i=0,L` are covered separately.
- For every `g ≥ 2`, the complete admissible source word `(1,10,8),18^g,(8,10,1)` of width `g+6` has exact actual nonoverflow successor `(3,0,18,17),18^(g-2),(17,18,0,3)`. A positive-integer realization exists, and that integer and its first two reverse-and-add successors are nonpalindromic.
- This does not prove that the family is closed under the update, that births regenerate infinitely, that any infinite orbit is nonpalindromic, or that 196 or another number is Lychrel. The `g` quantifier describes one-step instances of arbitrary finite size, not time.

## Definition and index checks

The foundation's `DecimalDigits.value` evaluates as `d i * 10^i`, so every index is indeed low-end first. `carry q 0=0` and `carry q (i+1)=(q i+carry q i)/10`. The branch of `nextColumns` is determined by actual `carry q L`, not a freely chosen overflow bit.

`Admissible` includes nonempty width, positive outer coefficients, physical-column bound 18, reflection symmetry, and parity at a self-reflecting center. It constrains only the first L columns; the review does not confuse the infinite function tail with decimal digits. The foundation's `valid_word_realizable` provides a positive integer and canonical decimal-digit realization, so these are not examples with abstract symbolic admissibility alone.

The nonoverflow formula uses `carry q i` and `carry q (L-1-i)`, the respective incoming carries of the two actually normalized digits; the latter is not incorrectly written as `carry q (L-i)`. Their bit bounds follow from `carry_bounded` and Admissible. At center `i=L-1-i`, the two coincide and the old value must be even, exactly excluding 9. L=1 is also covered, and the extra conditions do not incorrectly permit a central 9.

After overflow the width is L+1, the interior reflected position is `L-i`, and symmetry rewrites its old coefficient as `q (i-1)`. The formula therefore uses adjacent old columns `x=q(i-1),y=q i`, with carries `b=carry q i,d=carry q (L-i)`. The forward recurrences of both carries are established explicitly in Lean. `0<i<L` supplies every bound needed for truncated natural-number subtraction. At L=1 there are no interior columns, but both actual endpoints remain covered. The birth definition explicitly excludes an old adjacent pair already equal to the same extreme, matching this overflow ancestry convention; it cannot be transferred unconditionally to the same-position nonoverflow birth definition.

## All-parameter family and numerical safety

Using the exact column equation, admissible output digit bounds, and induction on recursive carries, `actual_carry` proves that the displayed incoming-carry template equals actual carry instead of assuming realizability. `actual_output` and `no_overflow` then supply the actual digits and actual branch; `actual_update` covers every physical column.

At an odd-width self-reflecting center, the source lies in the 18 core and satisfies parity. At `g=2`, the residual core interval is empty, but the successor still has two newborn singleton 18s adjacent to 0/17. At `g=3`, the residual core is exactly one central 18. `exact_18_positions` excludes extra 18 positions, so the description of two new singletons and an old core shortened by 2 does not depend on local formulas omitting boundary cases.

`numeric_canonical_next` simultaneously proves the successor's width, digit bounds, nonzero most significant digit, and value equality. `numeric_two_steps_safe` separately proves that n, step n, and step(step n) are nonpalindromic. For the input, outer column sum 1 excludes equal endpoint digits; for the two successors, the exact BadWord predecessor criterion is used. Private `numeric_safe` supplies only this finite-step bridge, with no hidden invariance premise.

Independent finite cross-checks also covered all Admissible symmetric words of widths 1..6, totaling 10,467 words and 58,041 physical columns, plus integer realizations of the family at g=2..100; all passed. The script/report is `semantic_check.py/json`. This is an independent semantic sanity check, not the proof of the universal Lean theorem. One realization at g=2 is `19899010 → 20998901 → 31988803`.

## Independent rebuild and tool audit

The reviewer ran the following command, rebuilding the foundation and three target modules in a previously nonexistent/empty independent directory, without using the author's existing `.olean` files:

```sh
LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so python3 proofs/contributions/agent-106/run-births/check.py --lean /workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean --build-dir /workspace/scratch/50e90e07524e/independent-agent106-build-001 --evidence-dir proofs/contributions/agent-106/run-births/review/independent/build-001 --modules NoOverflowBirths BirthFamily OverflowBirths
```

`check.py` was reviewed section by section; its hash is recorded in verification.json:

1. Reject a nonempty build directory; copy `.lean` files, not objects; set `LEAN_PATH` only to the new build directory and clear two other Lean source/sysroot environment overrides. Std comes from the specified Lean 4.19.0 installation.
2. Check the actual compiler version and pin the entire foundation source SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. Strip comments from the exact import dependency closure and reject sorry, admit, native_decide, axiom, unsafe, and sorryAx.
3. Actually run Lean on each module in the independent directory, preserving exact commands, exit codes, source/log SHA-256 hashes, and elapsed times. Also verify that source files did not change during compilation. A source-text scan is not treated as successful execution.
4. Generate a separate `AllAxioms.lean` with `#print axioms` for all 51 public theorems and 5 public definitions. Manually compare against source to confirm complete declaration enumeration. The matched output set must equal all 56 listed items exactly; accept only `propext, Classical.choice, Quot.sound` and reject sorryAx, ofReduceBool, trustCompiler, and similar entries.
5. Private theorems are not separately listed in the public inventory, consistent with the exported-theorem scope. Their axiom dependencies remain covered by each user's transitive `#print axioms`. The 1 private proof in BirthFamily and 2 in OverflowBirths were also read; all are explicit kernel proofs.

The specified preload shim source was also read. It maps only this process's readlink for `/proc/<pid>/exe` to `/proc/self/exe` to locate the runtime; it does not alter Lean source, proofs, or the kernel. The actual preload binary hash is recorded in verification.json, and the reviewer did not replace it.

Every formal-result subcommand, exit status, and complete log is in `build-001/`. This report's passing scope applies only to the exact byte versions pinned by source_inventory.json and that build report.
