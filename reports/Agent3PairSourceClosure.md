# Two-step correlated centre sources: an all-width rec2 pruning rule

**PAPER PROOF** (with a finite 48-residue arithmetic check). This result is a *necessary* restriction for a returned centre of the decimal period-8, spatial-period-48 lattice. It neither proves nor refutes existence of a periodic centre, nor does it certify a decimal Lychrel number. The two-step source relaxation is not a SAT solver or a complete model of a centre.

## 1. Exact source law already established

Use the physically correlated-carry boundary-flux theorem in `reports/Agent3CentreBoundaryFlux.md`, not independent fictitious carries. For a lower-half cut `L` frozen inside the lattice, write

`Q_t = sum_{i=L}^{ceil(n_t/2)-1} 10^i P_t[i] (mod 99)`.

At each step, `Q_(t+1) = A_t Q_t + X_t(L) + Z_t (mod 99)`, with `A_t=11` for overflow `g_t=1`, otherwise `A_t=2`. The exterior source `X_t(L)` is determined by the rec2 lattice and its two carry streams. The physical midpoint source `Z_t` has four cases, with `h=ceil(n/2)`, `R=h-1`, `q=10^R`:

| Input parity, overflow | Midpoint source `Z` modulo 99 |
|---|---|
| even, 0 | `-9 q c_h` |
| odd, 0 | `q(c_R-10c_h)` |
| even, 1 | `10 q O_h` |
| odd, 1 | `q(-10P_R-9c_h)` |

For the rec2 overflow schedule `10101010`, group each overflow step with its following no-overflow step. The pair multiplier is `22`, and its total source is `2X_(2j)+X_(2j+1)+2Z_(2j)+Z_(2j+1)`.

## 2. Physically correlated two-step source alphabets

**PAPER PROOF.** Let `q_*` be `10^h` if the pair starts at even length `n=2h`, or `10^(h-1)` if it starts at odd length `n=2h-1`. In the actual two-step evolution, the *normalized midpoint contribution* `V=(2Z_t+Z_(t+1))/q_* (mod 99)` obeys the following exact **outer** alphabets:

- **Even-start pair:** `V=2d+u-10[d>=5]`, where `d=O_h in {0,...,9}` and `u` is the incoming carry at the new odd-length midpoint. Thus `V in {0,...,9}`. The set has 10 residues.
- **Odd-start pair:** the old central coefficient is `P_(h-1)=2k`, `0<=k<=9`, and its outgoing carry is `e=[k>=5]`. The following even-length midpoint outgoing carry `v` is a bit. Thus `V=-40k-18e-9v (mod 99)`. This gives exactly 20 residues; its projection modulo 11 is **all 11 residues**.

These relations use actual central carry correlations **within each two-step pair**. The DP below relaxes only correlations *between different pairs*, making its reachable set an over-approximation of genuine centres. The even-start alphabet covers every residue modulo 9, as does the odd-start alphabet (its `-40k` term cycles through all residues as `k=0..8`).

**Why the alphabets hold.** For even `n`, the overflow creates an odd-length output with centre coefficient `2d`; its next outgoing carry is `[2d+u>=10]=[d>=5]`, giving the first expression. For odd `n`, the old middle coefficient is even `2k`; because base 10 is even, its outgoing carry is exactly `[k>=5]` regardless of its incoming bit. The next step starts with even length and its midpoint source is `-9q_*v`, giving the second expression. Both expressions are exact for all physical trajectories; treating the newly entering midpoint carry as free only enlarges the possibilities.

## 3. Sharp 192k-step source-only DP

For the rec2 lattice, `g=(10)^4`, so a compatible returned centre has temporal period `T=192k`, `k>=1`, and the lower-half length grows by `48k`. Every 48-cell rec2 lattice row has weighted charge zero modulo 99, so a returned bounded centre satisfies `Q_T=Q_0 (mod 99)` at any fixed frozen cut. The `96k` paired updates have multiplier `22`; modulo 9 it is invertible (`22=4`), while modulo 11 it is zero.

After the first pair the relaxed source sum has all nine residues modulo 9, for either input parity. At the second pair, the earlier sum can therefore supply **any** residue modulo 9, while the *last* pair source determines the residue modulo 11. By the Chinese remainder theorem, after any two or more pairs the exact relaxed reachable source set has size **99** if the last pair starts at odd length (its 20-element alphabet covers all modulo 11), or **90** if the last pair starts at even length (its 10-element alphabet misses exactly one modulo-11 residue). The fixed exterior source translates the set and does not change cardinality. This argument proves the DP cardinalities for every `T=192k`, not only a finite enumeration.

For initial lengths `n_0=400+o`, `o=0,1,2,3`, the last pair at `T=192k` starts at odd length for `o=0,2`, giving all 99 residues and **no** source-only closure obstruction. For `o=1,3`, the last pair starts at even length, giving 90 residues and a single forbidden modulo-11 class.

## 4. Concrete rec2 centre-defect exclusion

Let `F_t(i)` be the actual rec2 exterior (`B_t` then periodic `W_t`). For a cut `L` inside the frozen lattice and at least four lattice cells away from the centre, define

`D_0 = sum_{i=L}^{h_0-1} 10^i(P_0[i]-F_0(i)) (mod 11)`, `h_0=ceil(n_0/2)`.

Because every rec2 row has at most two consecutive coefficients equal to 9, the descending carry is forced to the unique periodic bulk carry within three frozen cells; hence the exterior source really is the prescribed `X_t(L)`, independently of centre width. The defect `D_0` does not depend on the choice of such a cut. The bulk charge over the extra 48k cells vanishes, so `Q_T=Q_0` under a genuine centre return.

**Corollary (PAPER PROOF + finite exact rec2 arithmetic):** for every returned bounded centre of any width and period `192k`, with the rec2 exterior and initial length `n_0=400+o+96r` (`r>=0` sufficiently large to separate the centre from the exterior),

`o in {1,3}  ==>  D_0 != 8 (mod 11)`.

For `o=0,2`, the same two-step source relaxation allows all 99 source residues and gives no exclusion.

**Finite rec2 check.** Let `X_6(L),X_7(L)` be the exterior sources at phases 6 and 7, and `h_*=(n_0+95)/2` the half-length at the final even-start pair for one 192-step lap (for `o=1,3`; replace 95 by `96k-1` for `k` laps). Modulo 11, closure forces `Q_0` to avoid `2X_6(L)+X_7(L)-10^(h_*)`. The supplied rec2 arrays satisfy, for all 48 spatial cuts `L=13,...,60` and both odd classes,

`2X_6(L)+X_7(L)-10^(h_*) - sum_{i=L}^{h_0-1} 10^i F_0(i) = 8 (mod 11)`.

This is checked with exact integer arithmetic at every cut; no search cap or statistical inference is involved. Because the exterior has spatial period 48 and zero 48-cell charge, the same identity holds for all larger lengths preserving the lattice phase. The result excludes only the **one specified centre-defect residue**; the other ten residues are *not* certified to correspond to a real centre.

## Reproduction and limitations

Run `python3 calculation/decimal_frontier/lattice_kinks/code/agent3_pair_source_closure.py calculation/decimal_frontier/lattice_kinks/data/lat2.txt` (standard library). The script checks all 48 spatial cuts, four initial length classes, and 192/384/576-step relaxed closures; it independently checks 400 physical four-step rec2 centre windows (1,600 exact carry transitions), including the fixed-cut boundary identity and the paired midpoint alphabets. The proof handles all `k>=1` via the two-step CRT argument. No Lean verification, base-10 certificate, actual periodic-centre witness, or unrestricted all-width nonexistence is claimed.
