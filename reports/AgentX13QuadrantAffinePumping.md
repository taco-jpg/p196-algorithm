# X13: guarded affine-counter reverse-and-add certificate oracle

**PAPER PROOF (format and exactness):** the guarded affine-run oracle described below proves universal one-step identities over unbounded integer *orthants*, using no sampling. **COMPUTED:** its Python implementation verifies an exact, genuinely two-independent-counter six-edge decimal transport and reproduces the published base-9/base-50 certificate cycles. **No Lean formalization or decimal infinite certificate is claimed.**

## Concrete new positive decimal mechanism

Use least-significant-first palindromic *pairwords* (each coefficient is a sum of the corresponding two digits). Write `Fold(H)=H++reverse(H)` if even, and `Fold(H)=H++reverse(dropLast(H))` if odd. For **every** pair of independent integers `k,l>=6` (not restricted to `k=l`), the following seven states form six exact consecutive base-10 reverse-and-add pairword transitions. Columns specify `H_t(k,l)=L ++ u^(k-a) ++ J ++ v^(l-b) ++ R`:

| t | L | u | a | J | v | b | R | odd? |
|---|---|---:|---:|---|---:|---:|---|---|
| 0 | 10 | 8 | 0 | 5,11 | 16 | 0 | 8 | no |
| 1 | 1,9 | 16 | 1 | 13,7,9 | 14 | 1 | 15,16 | yes |
| 2 | 3,9,13 | 14 | 2 | 7,16,9,9 | 10 | 2 | 12,14 | yes |
| 3 | 7,9,7 | 10 | 3 | 9,16,13,0,0 | 2 | 2 | 6,10 | yes |
| 4 | 14,18,15,1 | 2 | 4 | 0,14,7,1,0 | 4 | 2 | 13,0 | yes |
| 5 | 5,14,15,7,3 | 4 | 5 | 2,5,12,8,1,4 | 8 | 2 | 4 | no |
| 6 | 11,9,11,15,6 | 8 | 5 | 4,11,4,17,2,8 | 16 | 2 | 8 | no |

Overflow bits are `100010`; input length `2k+2l+8`, final length `2k+2l+10`. The *two* independently chosen central plateaux return to bulk symbols `(8,16)` at t=6 but with lengths `k-5` and `l-2`, creating a **two-dimensional differential shear** rather than N19's previously tested synchronized diagonal `k=l`. The boundary words and centre do **not** return to t=0, and the two plateau counters decrease, so this is not yet a renewable cycle. All seven pairword phases contain odd coefficients, excluding palindromic decimal values throughout these six edges. This is a positive finite mechanism, not a no-go result.

## Exact symbolic oracle (not a large-sample inference)

A symbolic word is a finite concatenation of patterned runs `pat[(offset+i) mod m]` of integer-affine lengths `a*k+b*l+c`; `offset` may itself be affine. The guard here is the infinite quadrant `k>=K, l>=L`. For any affine difference `D`, the checker proves `D>=0` everywhere only when both slopes are nonnegative and `D(K,L)>=0`. Incomparability causes an explicit `Nonuniform` exception, not an arbitrary branch. All currently accepted claims are uniform on the **entire** quadrant.

For each run, normalize coefficients by the exact finite carry recurrence `d=(v+c) mod base`, `c'=floor((v+c)/base)` with `c in {0,1}`. A whole pattern induces a monotone Boolean map on carries; any monotone map of `{0,1}` is constant or identity, so its output carry is fixed after the **first complete copy**. Generate (1) first-period digits, (2) an affine-length repeating steady part, and (3) the remaining partial final period with its actual carry. The partial period is important: leaving it out produces a false base-9 edge, detected and fixed during development. For every run, the checker demands an exact constant residue of its length modulo its spatial period.

Reverse the resulting symbolic digit word by reversing both run order and patterns and updating the affine phase offset. To compute the next pairword, zip this word against its symbolic reversal. Every comparison of two remaining run lengths must be ordered for all `(k,l)` in the guard. For each overlap with pattern lcm `m`, the checker either proves overlap length at least `m` throughout the quadrant and compares **all m residues**, or proves the length is a fixed integer shorter than `m` and checks exactly those positions. Unsupported intermediate cases fail closed. A second symbolic zip proves equality with the proposed target, checking every occurring residue. All 277 comparisons of the six decimal edges are proved uniformly; they are **not** evaluated at a finite table of `(k,l)` samples.

**Soundness (PAPER PROOF).** Induction over the concatenated runs proves normalization is exact for every guard valuation: the first/steady/remainder decomposition and idempotent carry map guarantee the actual digit output and carry at every position. Induction over two-sided run splits proves the zip is pointwise exact: comparisons hold universally, and all relevant periodic residues are checked. Thus every accepted one-step identity holds for **all** guard values. No SAT/SMT soundness assumptions are needed for this restricted orthant oracle, and unsupported comparisons are rejected.

**Certificate format (PAPER PROOF, conditional on finding a cycle).** Give each phase a folded affine-run pairword `P_v(z)` with integer counter vector `z`, a guard `G_v={z: A_v*z>=c_v, z congruent r_v mod m_v}`, and a nonpalindrome witness. Each directed edge carries a counter-affine map `z' = M_e*z+d_e`, a universal exact step proof (the oracle or a separately checked Presburger proof), and `M_e*G_v+d_e subset G_w`. If a finite directed cycle returns to the same phase, has a nonempty forward-invariant guard, and starts from a realizable canonical integer, induction proves an infinite nonpalindromic orbit. For a translation-only cycle over an orthant, it suffices that the total counter drift is componentwise nonnegative and that all intermediate counter guards are respected. This is a checkable *ranking/cone* obligation and accommodates unequal moving-band lengths rather than requiring `k=l`. Our executable checker handles the orthant identity obligations; generic Presburger/polyhedral guard checking is specified but **not implemented**.

**Lean 4 proof sketch (NOT Lean-verified):** define `Aff : Nat -> Nat -> Int`, `Run` with a nonempty periodic word and affine length, and `expand : Params -> List Run -> List Nat`. Prove `norm_period` via the three possible monotone Boolean carry maps, `zip_periodic_sound` by interval partition and LCM residue completeness, then `edge_sound` from `decide (oracle ...) = true`. A `guarded_cycle_sound` induction over integer time uses counter guard preservation and `pairs(normalize(P))`; the existing `LatticeBand.Cert.lean` is a proven one-counter absorbing special case. Lean 4.19/`lake` and repository-wide `tools/verify.py --changed` could not be run locally (GitHub shell checkout blocked by DNS), so **no Lean files are committed**.

## Controls, tests and limitations

- **Base 9** published `LatticeBand.Base9` cycle: `|B|=61`, `W=[1,1,15,15]`, band length `4k+2`, `k>=3`. All 10 edges symbolically accepted; overflows `1100011000`; cycle returns with `k->k+1` and 2,554 universally justified run comparisons. This duplicates the known positive result as a *control*, not as a new theorem.
- **Base 50** published `Agent10Base50NeutralCycle`: `|B0|=36`, neutral `49` band, centre length 8, `k>=12`. All four edges symbolically accepted; overflow `0101`; phase band offsets `(0,1,0,2,1)`; cycle returns `k->k+1`, 653 universal comparisons. Again a control, not a new base result.
- **Decimal two-counter:** all six edges, `k,l>=6`; independent *ordinary integers* at `(6,6),(6,90),(97,6),(27,101),(1000,537)` agree at all seven states with a separate digit-array updater and a separately implemented pairword normalization. All displayed pairwords are nonpalindromic.
- **Mutation and generality controls:** an expected output coefficient mutation is rejected; an undecidable `k<=l` comparison is rejected. Another 125 randomized periodic one-step symbolic transformations were checked against independent finite digit normalization at 5 lengths each, zero discrepancies.

Reproduce: `python3 calculation/new_structures/agent-X13/test_oracle.py`; machine-readable summary in `data.json`. Code: `affine_two_counter.py` (decimal uniform two-independent-counter certificate data and checker), `periodic_affine.py` (general periodic symbolic carry/zip), and `controls.py` (independent known-positive lattice/neutral cycles).

**Exact limitations:** The checker refuses phase offsets depending on the counter residue or run-length comparisons whose sign changes inside the quadrant. A generic guarded-Presburger splitting backend, SAT/CEGAR synthesis, and Lean kernel formalization remain future work. The decimal six-edge path has nonrenewing boundaries and decreasing counter lengths; it **does not** certify any base-10 Lychrel number, 196, or an infinite nonpalindromic orbit. The concrete search redirection is to synthesize a *compensating return edge* from `H6` to `H0` with total counter drift in the nonnegative quadrant, then check it with this exact oracle.
