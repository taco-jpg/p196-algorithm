# Agent #105: exact high-return and two-output safety criteria

Task `agent105-high-return-criterion` was claimed in coordination commit
`61e2f7579eb710a729fe0b6a9ad2ff893ed715b4`. This extends the independently
audited actual high-return bridge in the sibling `actual-high-return/` package.

For an admissible decimal high word `q` of width `L`, let
`P = nextColumns q L`, `M = L+1`, and
`u_i = carry P i + carry P (M-1-i)`. These are the actual carries.
The exact two-step successor is high if and only if:

- the second addition does not overflow;
- `q_0 >= 14`;
- each `P_i` lies in `4..9` or `14..18`;
- at a coefficient 4 or 14, `u_i >= 1`;
- at a coefficient 9, `u_i <= 1`.

This covers every positive width, including overlapping and singleton cases.
The formula is an exact test on the whole finite word; it does not say that
independently chosen local carry bits or finite graph paths are realizable.

The safety result has a stronger domain than the original return-specific
written argument: for **every actual high initial word**, the first and
second positive outputs are both nonpalindromic if and only if some adjacent
source pair coefficients sum to at least 28. Equivalently, the actual first
successor pair word has a coefficient at least 10. No return premise is needed.
The initial integer and later outputs are outside this finite safety statement.

Status: **INDEPENDENTLY-REVIEWED**. The combined fresh build of all
11 modules passed, with transitive audits of all 357 explicit public
theorem/lemma declarations (14 new). Every command exited zero and source
hashes remained unchanged. Only `propext`, `Classical.choice`, and `Quot.sound`
were reported. No `native_decide`, `Lean.ofReduceBool`, custom axiom, or proof
placeholder occurs in the audited chain. Sources are pinned to commit
`8f846def03ec368d1de0fe20965f5e47f6172bc5` by
`verification/initial/source-publication.json`.

Agent #108 subsequently completed the previously pending independent gate.
Its review at `60806ee2a95c86463b2ea9a648b8afcd28f8563f` reports a separate
source-clean eleven-module rebuild and semantic review, dynamic audits of
1,309 local theorem constants, and actual `#print axioms` for all 1,258
exports, including generated auxiliaries. All commands and audits passed.
An additional official hosted run passed without the local runtime adapter.
See [the independent report](https://github.com/taco-jpg/p196-algorithm/blob/60806ee2a95c86463b2ea9a648b8afcd28f8563f/proofs/contributions/agent-108/review-agent105-criterion/REVIEW.md)
and `review/CrossAgentAcceptance.json` for exact evidence and the coordinator's
hash comparison of all eleven sources with the reviewed commit and main.

The earlier internal specialist's incomplete review and finite controls,
and `review/CoordinatorReview.md`, remain historical evidence; the later
cross-agent review supplies the gate they did not complete. Source entered
main through PR #15, but shared accepted-build/index registration is a
separate integration obligation and is not inferred solely from that merge.

From the repository root, using a fresh output directory:

```sh
python3 proofs/contributions/agent-105/high-return-criterion/check.py /path/to/lean-4.19.0/bin/lean --output-dir /tmp/agent105-criterion-review-new
```

Lean is the official 4.19.0 release, commit `6caaee842e94`. See the sibling
package's `runtime/` for this environment's disclosed startup shim.

The local and return formulas formalize the written section 2 of
`2026-10-15-full-high-return/FULL_HIGH_RETURN.md`; the exact second-output
adjacency theorem is reused from `HighCarryReduction`. The nearest-non-nine
rephrasing is not newly formalized here. No P196 or infinite safe orbit claim
is made. Agent #1's separate safe sharpness family is not duplicated.
