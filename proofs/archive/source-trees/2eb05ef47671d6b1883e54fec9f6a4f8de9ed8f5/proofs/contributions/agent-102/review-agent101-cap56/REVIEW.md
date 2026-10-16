# Independent replication of `agent101-exterior-cap56` (Agent #102)

Reviewed: Agent #101 result at `50ce5e3d43533463990bc73a604f1383a3f657dc`
(`proofs/contributions/agent-101/exterior-cap56/`). Replication only; no new theorem.
**Evidence label: checked finite computation (not Lean).**

**Verdict: REPLICATED.** Every reported number for caps 0–6 is reproduced exactly by a separately
written implementation, including the previously C-only cap 6.

## Independence

`outer_ref.py` (Python) and `outer_graph.c` (C) were written from
`2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md` (3), (4), (6), (7) and the sec. 6 suffix
trim, without reading Agent #101's `exterior_cap.c`, `exterior_ref.py` or `replay_py.py`. Only the
README's domain definition (even phases, canonical trimmed `B`, exit when `|B'| > cap`, exit time
counts the leaving step) was used. Traversal: functional-graph path following with an on-stack mark
(any revisit of an on-stack state aborts with CYCLE), byte-per-state memo; indexing is base-19 per
length and phase.

## Results

| cap | states | internal | exit | cycles | max exit time | argmax | #argmax |
|---:|---:|---:|---:|---:|---:|---|---:|
| 0 | 8 | 4 | 4 | 0 | 4 | c=2, B=() | 1 |
| 1 | 144 | 44 | 100 | 0 | 5 | c=2, B=() | 2 |
| 2 | 2,736 | 800 | 1,936 | 0 | 7 | c=14, B=(2,17) | 1 |
| 3 | 51,984 | 15,164 | 36,820 | 0 | 9 | c=8, B=(11,9) | 5 |
| 4 | 987,696 | 288,080 | 699,616 | 0 | 15 | c=2, B=(4,0,1) | 1 |
| 5 | 18,766,224 | 5,473,484 | 13,292,740 | 0 | 20 | c=10, B=(2,0,1,13,11) | 1 |
| 6 | 356,558,256 | 103,996,160 | 252,562,096 | 0 | 21 | c=10, B=(2,0,1,13,11) | 2 |

Exit-time histograms for caps 5 and 6 are in `cap5.out`, `cap6.out` (cap 6: 29 s, ~400 MB).
`py_cross.py` re-enumerates caps 0–3 with the Python map and agrees with the C program
(`py_cross_result.json`).

## Controls of the map

`outer_ref.py` checks the outer map against literal integer reverse-and-add of complete realized
templates (random phase in all 16, `|B| ≤ 7`, random `A`, symmetric `C`, `g ∈ 12..16`, `h ∈ 2..6`):
the next integer's width is `width + γ`, its mirrored-sum word begins with `B'`, followed by a run of
`c'` of length at least `g-2+γ`; and `B'` does not end in `c'`. 20,000 controls PASS
(`literal_controls.json`, seed 1020). The word-level identity (8) itself is Lean-checked by
Agent #109 (independently reviewed, `../review-agent109-step-bridge/`).

## Scope

The consequence "every complementary-band quotient cycle has `|B| ≥ 7` at some step" still rests on
the written projection bridge (gamma and `B'` depend only on `(c,B)`), which follows from Agent #109's
reviewed identity (8) plus the trim, but the trim/projection step itself is not Lean-checked here.
Larger exteriors remain UNKNOWN. Nothing about 196 or Lychrel existence follows.
