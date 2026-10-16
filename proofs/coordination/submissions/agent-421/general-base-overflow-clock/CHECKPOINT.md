# Agent #421 — verified overflow normalization and actual outer clock

Status: LEAN_CHECKED; independent semantic review and integration pending. New overflow exports: 29. Combined with the completed no-overflow package: 73 exported theorems, not 73 distinct original claims. All17 modules in the combined clean build returned exit0, and every exported theorem's transitive axiom audit passed. Only propext/Classical.choice/Quot.sound occur, or no axioms. No sorry/admit/native_decide/new mathematical axiom appears in the built source closure.

## Exact source and completed claims

Written source: proofs/research/resume_general_base_normalization_proof.txt at original commit 2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5. Inspected main: 9de08d78db6526e2ce2dd66cedd5e63f600424bd.

Completed here: low-zero/high-alpha/neutral overflow normalization, complete first-carry preservation, positive canonical same-width realization, exact fresh leading-one/actual-width bridge, and the universal outer schedule alpha->s (O,N) or (b-1)->b->1 (O,O,N). O is an actual digit-gaining reverse-add step; N is a non-digit-gaining step. A non-overflow step alone does not establish a palindrome.

Agent421Overflow.same_carries_actual_schedule includes the positive representative, every first-carry position, canonicality of three actual outputs, all three exact integer reverse-add value identities, and the exact widths L+1/L+1 or L+1/L+2/L+2. The quantifiers are universal in b,L,q before the existential representative. Source_bases_actual_schedule specializes to even b>=10 or odd b>=17. The representative need not equal the original seed.

Agent #422 owns the protected-neutral-run rule and endpoint closure. Those were not duplicated. Global protected-class preservation, interior low-bound propagation, and composition into the full four-step palindrome upper bound remain open in this contribution. No exhaustive repository census, independent approval, main mutation, merge, decimal Lychrel existence, or all-time196 theorem is claimed.

## Published exact proof sources

Complete overflow-source commit: 97b5274fe0b8d6772d9f89b9216327838899adb3, on existing p196/coordination. All four blobs were read back and match the clean-checked files:

- Agent421Overflow.lean: d2bee9aaebdb3669ec8f7092be482c29bd1ebd81
- Agent421OverflowNormalization.lean: 9565ad42466272226256af88b3610ae59cee6784
- Agent421OverflowClock.lean: 3ad359f1b50e0d5f67422d49bef31b5d6503fe37
- Agent421OverflowArithmetic.lean: f710e7844d8bdf2b581da7052102486c2ca0b5cd

The sibling no-overflow sources were published at 5bf4830d6d822eab08380937985e16f214ed2678 and also matched their checked blobs. The seven original dependencies retain their authorship and exact original Git blob pins in the sibling manifest.

## Actual verification and reproduction

Lean4.19.0, official commit6caaee842e94. Combined clean run: 2026-10-16T04:57:02.091997Z through 04:57:13.615438Z, seventeen successful module compilations. A second standalone clean run also passed all17 modules and the all73 audit using identical source hashes. Both are Agent421 self-rebuilds, not independent review. OverflowAudit.lean prints all29 new transitive axiom reports; axioms.log is the actual recorded output. The sibling verifier audits its44 exports.

From this directory, with both sibling submission folders present and a repository retaining original commit2eb05ef:

```sh
set -eu
SRC="$PWD"
LEAN=/absolute/path/to/lean-4.19.0/bin/lean
OUT=/tmp/agent421-new-combined-check
python3 ../general-base-nooverflow/verify.py --repo /absolute/path/to/repository --lean "$LEAN" --out "$OUT"
cp "$SRC"/Agent421Overflow*.lean "$SRC"/OverflowAudit.lean "$OUT/build/"
cd "$OUT/build"
export LEAN_PATH="$PWD"
for module in Agent421OverflowNormalization Agent421OverflowClock Agent421OverflowArithmetic Agent421Overflow; do
  "$LEAN" -o "$module.olean" "$module.lean" > "$OUT/logs/$module.log" 2>&1
done
"$LEAN" OverflowAudit.lean > "$OUT/logs/overflow-axioms.log" 2>&1
```

OUT must not already exist. Do not import the sibling's retained early Local.lean checkpoint as well as Agent421NoOverflowLocal.lean. The two explicit roots are Agent421NoOverflow.lean and Agent421Overflow.lean.

A full contribution-path Git patch, per-module logs, manifests, inventories, and an offline standalone package are retained in the Agent421 delivery. Local patch commit: bb6d9d436b7fbd0c20d32bb72141c39c317f9333; patch base2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5; patch SHA256 7f40c5f1bd4e2e07aa93c2cc63d18ad7be6fdaea1f4e5ca26bbe34d3a4148215. Only proofs/contributions/agent-421 paths are changed by that patch. Apply through the designated integration writer after review; never merge the entire coordination branch.
