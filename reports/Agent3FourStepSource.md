# Four-step physical centre-source cancellation in decimal reverse-and-add

**PAPER PROOF.** This is an exact all-width statement about physically correlated carries. It shows that the existing mod-9 centre-source closure condition is automatically satisfied in two rec2 initial-length classes. It is **not** a proof that a centre exists, and it does not exclude a centre or prove a base-10 Lychrel number.

## The theorem

Let `P_t` be the symmetric pair word of a genuine base-10 reverse-and-add orbit. Suppose the starting length `n_0` is **even** and the next four actual overflow bits are `g_0,g_1,g_2,g_3 = 1,0,1,0`. Let `Z_t` be the *physical midpoint source* in the exact weighted half-word boundary-flux identity of `reports/Agent3CentreBoundaryFlux.md`, with modulus `99`:

`Q_(t+1) = A_t Q_t + X_t + Z_t (mod 99)`, where `A_t=11` if `g_t=1`, otherwise `2`.

Then the **four-step accumulated centre source**

`S4 = 22(2Z_0+Z_1) + 2Z_2+Z_3`

is divisible by `9`, for every centre width and every choice of physical carries. In particular, for any even-length orbit segment with overflow word `(1010)^k`, the complete `4k`-step centre-source contribution is `0 (mod 9)`.

## Proof (no independent-carry relaxation)

Let `n_0=2h`, and let `d` be the actual normalized output digit at the new centre position `h` after the first overflow. From the exact even/overflow-1 source formula, `Z_0 = 10^h d (mod 99)`, hence `Z_0 = d (mod 9)`.

The first output has odd length `2h+1` and centre pair coefficient `2d`. At the next, no-overflow step, write `u` for the *actual* incoming carry into that middle coefficient. Its outgoing carry is `v=[2d+u>=10]=[d>=5]`. The odd/no-overflow source is `Z_1=10^h(u-10v) (mod 99)`. Define `e=2d+u-10v`, the actual normalized centre digit after this second step. Thus

`2Z_0+Z_1 = e (mod 9)`.

The second output still has odd length and centre pair coefficient `2e`. At the third step (`g_2=1`), the odd/overflow-1 midpoint source is `Z_2=-10^h(10*(2e)+9c) (mod 99)` for its actual outgoing carry `c`, so `Z_2=-2e (mod 9)`. The third output has even length, and the fourth step has no overflow, so the even/no-overflow source `Z_3=-9*10^R*c'` is `0 (mod 9)`.

Consequently `S4 = 22e + 2(-2e) = 18e = 0 (mod 9)`. All four source formulas are the previously proved exact physical-carry formulas, and the only new relation is the *shared actual centre digit* `e` between the second and third steps. No centre-periodicity assumption was used.

After four steps the length has increased by two and is even again. Therefore the same cancellation holds independently in every successive four-step block with overflow word `1010`, and multiplication by intervening step factors preserves divisibility by 9. This proves the general `(1010)^k` statement.

## Consequence for the decimal p8/m48 rec2 lattice

The rec2 overflow word is `(1010)^2`, and every compatible centre return has period `T=192k`. In initial length classes `n_0=400+o+96r`, `o=0,2`, the length is even at every four-step block boundary. Hence the *entire central source* in the 192k-step boundary-flux closure is `0 (mod 9)` **identically**, regardless of centre width or internal digits. The previously proved rec2 exterior source is also `0 (mod 9)` at all 48 lattice cuts (see `reports/Agent3CentreBoundaryFlux.md`). Thus the necessary mod-9 condition on total source from that report is automatically true for `o=0,2` and cannot provide an all-width obstruction in those classes. This does not say anything about the existence of a real returned centre, or about other moduli.

## Finite exact sharpness control (COMPUTED, not a centre census)

`calculation/decimal_frontier/lattice_kinks/code/agent3_fourstep_source.cpp` enumerates **every** central free half-word of width exactly 5 against the stored rec2 exterior, with initial lengths `400+o` for all four `o`. The other coefficients are the exact rec2 lattice and its mirror, and the centre coefficient is constrained even when the input length is odd. Each candidate is replayed by the direct schoolbook pair-word carry algorithm for four steps; the prescribed overflow schedule is checked. The enumerator is restartable through optional local checkpoint files (not committed).

| initial `o` | enumerated centre words | distinct `S4 mod 99` |
|---|---:|---:|
| 0 | 2,476,099 (`19^5`) | **11**, exactly `{0,9,18,...,90}` |
| 1 | 1,303,210 (`19^4*10`) | **90** |
| 2 | 2,476,099 (`19^5`) | **11**, exactly `{0,9,18,...,90}` |
| 3 | 1,303,210 (`19^4*10`) | **90** |

Thus the even-start universal upper bound of 11 residues is *attained* by genuine four-step rec2-centred pair-word evolutions of width 5. The odd-start counts are controls only; their 90-residue restriction is already accounted for by the earlier paired-source theorem `reports/Agent3PairSourceClosure.md`. No four-step survivor is asserted to return or to persist indefinitely.

Reproduce from repository root:

`c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/code/agent3_fourstep_source.cpp -o /tmp/agent3_fourstep`

`/tmp/agent3_fourstep calculation/decimal_frontier/lattice_kinks/data/lat2.txt /tmp/agent3_fourstep_state`

The code uses no external libraries and runs one process, with constant-size residue storage and bounded digit vectors. The PAPER PROOF is width-independent; the finite width-5 enumeration demonstrates sharpness but does not claim an all-width census, a periodic centre, or a decimal certificate.
