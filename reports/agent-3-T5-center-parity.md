# Agent 3 — T5: arbitrary-width center-length parity obstruction

**Status: PAPER PROOF; COMPUTED independent controls, NOT LEAN-VERIFIED.** This is a universal necessary condition for the **signed two-neutral-band certificate format** developed in Agent 3's draft [#320](https://github.com/taco-jpg/p196-algorithm/pull/320). It is *not* a base-10 Lychrel theorem, nor a general rejection of two-band certificates. This is separate from the bounded graph negative in [#359](https://github.com/taco-jpg/p196-algorithm/pull/359).

## Exact scope

For any integer base `b>=2`, take ordinary base-b digit blocks `A,B,M,D,E` with `|A|=|E|>=1` and `|B|=|D|` and neutral digit runs `x^g,u^h,v^h,y^g`, where `x+y=u+v=b-1`. The full phase is

```text
W(g,h)=A x^g B u^h M v^h D y^g E.
```

The signed format checks full-word reverse-add output from the five fixed-block carry addition, then uses an *arbitrary finite number of actual digit-preserving signed boundary moves*. Each signed step has two matched run gains `delta_g,delta_h` (possibly negative). This theorem does **not** rely on a limit on the number or size of moves, nor on any fixed-block width upper bound.

## PAPER PROOF 1: center parity changes exactly on leading overflow

Write `a=|A|=|E|`, `d=|B|=|D|`, `m=|M|`, and `F=2a+2d+m`. The fixed-block part of the exact reverse-and-add image has length `F+f`, where `f in {0,1}` is the leading carry from adding `A` to `reverse(E)` after the preceding incoming carry. The four neutral output runs have respective lengths `g,h,h,g`, unchanged by carry transmission.

A valid signed edge with gains `(delta_g,delta_h)` is a literal digit-word equality with the next phase. Hence **word lengths** agree:

```text
F+f+2g+2h = F' + 2(g+delta_g) + 2(h+delta_h).
F'−F = f − 2(delta_g+delta_h).
```

Since the difference of the doubled outer-block lengths is even, taking both sides modulo 2 gives

```text
m'−m ≡ f (mod 2).
```

Thus **an edge has leading carry 1 if and only if its middle fixed block length changes parity**. This is a purely mathematical identity for every accepted signed edge. It does not require any graph enumeration, period bound, positive-sign moves only, or Lean assumptions.

## PAPER PROOF 2: empty M has no signed successor

When `M` is empty, its zero-width fixed addition simply transmits its incoming carry: `c3=c2`. The two output inner run digits are respectively `(b−1)(1−c3)` and `(b−1)(1−c2)`, and therefore equal. A valid successor phase requires that they sum to `b−1`. Two equal elements of `{0,b−1}` cannot sum to `b−1` for any `b>=2`. Therefore **no valid phase with empty M can have a successor edge** in this format.

## PAPER COROLLARY: every positive-gain cycle needs two central parities

For any closed phase itinerary, summing `F'−F=f−2(delta_g+delta_h)` gives

```text
2 * sum(delta_g+delta_h) = sum(f).
```

A positive-gain signed certificate has `sum(delta_g)>=0`, `sum(delta_h)>=0` and their sum strictly positive, so the leading carry is 1 at least twice. Therefore central-length parity must change. Since no phase can have `m=0` on a closed itinerary, a positive-gain cycle **must visit both an odd middle-block length `m>=1` and an even middle-block length `m>=2`**.

In particular, **if every phase has `|M|<=1`, no positive-gain signed certificate exists, for ANY base, period, widths of A/B, boundary move magnitudes or number of boundary operations.** This strictly subsumes the separate width-bounded `|A|<=2,B=D=empty,|M|<=1` experiment below. It does not exclude cycles where M alternates between odd and even lengths, nor a novel format where the fixed-block/run split can change in another way.

## COMPUTED controls (not an alternative proof)

Standalone script, Python 3 standard library only:

```sh
python3 calculation/agent-3/center_parity_controls.py
```

Locally observed:

```text
positive_binary_parity_controls 4 EDGES PASS carry [0, 1, 0, 1]
base10_nonclosed_parity_control 3 LENGTHS PASS
independent_bigint_crosschecks 24000 PASS; empty_center_rejections 3875
```

The known base-2 four-phase positive witness in #320 has central lengths `4 -> 4 -> 3 -> 3 -> 4` and leading carries `0,1,0,1`, exactly as the lemma predicts; this witness was already established through another Lean certificate. A separately checked *nonclosed* decimal two-band edge changes central length `5 -> 4` with leading carry 1. Random independent ordinary big-integer reverse-add and carry tests cover bases 2, 3, 10, 11, 17, 26, 24,000 cases. Of these, 3,875 empty-middle cases independently reject complementary output inner runs.

A disjoint **COMPUTED finite sanity check** from the earlier all-order graph implementation: base10, all fixed decimal digits, `|A|=|E|<=2`, `B=D=empty`, `|M|<=1`, one signed move per boundary in `{-1,0,1}` in any order: **399,960 states, 181,800 complementary-run source images, 266,220 directed edges, 399,960 peeled, zero cyclic residual** (exit 0, 28.33s wall / 252,816 KB peak RSS). The PAPER theorem excludes all positive-gain closed cycles in this and every larger `|M|<=1` family, independent of this finite graph.

No new Lean module, axiom, or registry entry; `python3 tools/verify.py --changed` **NOT RUN** without a complete repository checkout. This is a DRAFT review claim. Explicitly **NOT claimed**: decimal Lychrel existence, unrestricted decimal two-band impossibility, all-signed-format acceptance in Lean, a kernel theorem, or any implication to the original one-neutral-band checker.